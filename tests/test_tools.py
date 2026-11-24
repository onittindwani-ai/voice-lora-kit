import json
import tempfile
import unittest
from pathlib import Path

import _path  # noqa: F401  (sets up sys.path)
import build_dataset
import check_data
import check_machine
import common
import compare
import fuse
import style_check
import train

ROOT = _path.ROOT
CARD = json.load(open(ROOT / "data" / "style-card.bluebird.json", encoding="utf-8"))


class CheckMachine(unittest.TestCase):
    def test_apple_silicon_16gb_gets_the_small_model(self):
        result = check_machine.assess("Darwin", "arm64", 16.0, 50.0, (3, 12))
        self.assertEqual(result["verdict"], "ok")
        self.assertIn("1.5B", result["model"])
        self.assertIn("TESTED", result["model_status"])

    def test_small_memory_gets_the_tiny_model_and_an_untested_label(self):
        result = check_machine.assess("Darwin", "arm64", 8.0, 50.0, (3, 12))
        self.assertIn("0.5B", result["model"])
        self.assertIn("UNTESTED", result["model_status"])

    def test_windows_is_not_supported_here(self):
        result = check_machine.assess("Windows", "AMD64", 32.0, 100.0, (3, 12))
        self.assertEqual(result["verdict"], "not_supported_here")
        self.assertIsNone(result["model"])

    def test_low_disk_and_old_python_are_flagged(self):
        result = check_machine.assess("Darwin", "arm64", 16.0, 2.0, (3, 9))
        self.assertEqual(result["verdict"], "ok_with_notes")
        self.assertEqual(len(result["notes"]), 2)


class BuildDataset(unittest.TestCase):
    def test_duplicates_are_dropped_case_and_space_insensitive(self):
        rows = [("Are you open?", "a", "normal"), ("are  you OPEN?", "b", "normal"), ("Other", "c", "normal")]
        kept, dropped = build_dataset.drop_duplicates(rows)
        self.assertEqual(dropped, 1)
        self.assertEqual(len(kept), 2)

    def test_private_data_is_found(self):
        rows = [("Call me on 555 123 4567", "ok", "normal"), ("write to bob@example.com", "ok", "normal"), ("clean", "clean", "normal")]
        labels = [label for _, label in build_dataset.find_private(rows)]
        self.assertIn("a phone number", labels)
        self.assertIn("an email address", labels)
        self.assertEqual(len(build_dataset.find_private([("clean", "clean", "normal")])), 0)

    def test_prices_and_times_are_not_flagged_as_private(self):
        rows = [("A large cake is $68 and serves 16, open 8am to 4pm", "ok", "normal")]
        self.assertEqual(build_dataset.find_private(rows), [])

    def test_example_has_system_user_assistant(self):
        example = build_dataset.to_example("facts", "q", "a")
        self.assertEqual([m["role"] for m in example["messages"]], ["system", "user", "assistant"])
        self.assertEqual([m["role"] for m in build_dataset.to_example("", "q", "a")["messages"]], ["user", "assistant"])

    def test_default_split_sizes(self):
        valid, test = build_dataset.split_counts(70, None, None)
        self.assertEqual((valid, test), (6, 6))
        self.assertEqual(build_dataset.split_counts(70, 3, 2), (3, 2))

    def test_exam_always_gets_unknown_questions(self):
        rows = [(f"q{i}", f"r{i}", "unknown" if i % 4 == 0 else "normal") for i in range(80)]
        test, valid, train = build_dataset.stratified_split(rows, 10, 8, seed=7)
        self.assertEqual((len(test), len(valid), len(train)), (10, 8, 62))
        self.assertGreaterEqual(sum(1 for r in test if r[2] == "unknown"), 3)
        self.assertEqual(len({r[0] for r in test + valid + train}), 80)  # nothing lost, nothing doubled

    def test_few_unknown_rows_do_not_force_any_into_the_exam(self):
        rows = [(f"q{i}", f"r{i}", "unknown" if i < 3 else "normal") for i in range(60)]
        test, _, _ = build_dataset.stratified_split(rows, 6, 4, seed=1)
        self.assertEqual(len(test), 6)


class SampleDataEndToEnd(unittest.TestCase):
    """The shipped sample must build, validate, and follow its own style card."""

    def test_sample_builds_and_validates(self):
        import contextlib
        import io
        import sys

        with tempfile.TemporaryDirectory() as tmp:
            argv = ["build_dataset", "--csv", str(ROOT / "data" / "sample_customer_replies.csv"),
                    "--system-file", str(ROOT / "data" / "FACT-SHEET.txt"), "--out", tmp]
            old = sys.argv
            sys.argv = argv
            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    code = build_dataset.main()
            finally:
                sys.argv = old
            self.assertEqual(code, 0)
            with open(Path(tmp) / "split-summary.json") as handle:
                summary = json.load(handle)
            self.assertEqual(summary["train"] + summary["valid"] + summary["test"], 80)
            self.assertGreaterEqual(summary["unknown_rows_in_test"], 3)
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(check_data.main(tmp), 0)

    def test_every_sample_reply_follows_the_style_card(self):
        import csv

        with open(ROOT / "data" / "sample_customer_replies.csv", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 80)
        full, total, _ = style_check.score(CARD, [r["reply"] for r in rows])
        self.assertEqual((full, total), (80, 80))

    def test_every_unknown_sample_reply_admits_it_must_check(self):
        import csv

        with open(ROOT / "data" / "sample_customer_replies.csv", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        unknown = [r for r in rows if r["kind"] == "unknown"]
        self.assertEqual(len(unknown), 23)
        self.assertTrue(all(style_check.says_check_first(CARD, r["reply"]) for r in unknown))


class CheckData(unittest.TestCase):
    def _folder(self, train_rows, valid_rows, test_rows):
        tmp = tempfile.TemporaryDirectory()
        for name, rows in (("train", train_rows), ("valid", valid_rows), ("test", test_rows)):
            common.write_jsonl(Path(tmp.name) / f"{name}.jsonl", rows)
        return tmp

    @staticmethod
    def _row(question, answer="reply"):
        return build_dataset.to_example("", question, answer)

    def test_leak_between_train_and_test_is_an_error(self):
        train_rows = [self._row(f"q{i}") for i in range(25)]
        tmp = self._folder(train_rows, [self._row("v1")] * 4, [self._row("q3")] * 4)
        import contextlib
        import io

        with contextlib.redirect_stdout(io.StringIO()) as out:
            code = check_data.main(tmp.name)
        self.assertEqual(code, 2)
        self.assertIn("cheating", out.getvalue())

    def test_last_message_must_be_the_assistant(self):
        errors, _ = check_data.check_rows("train", [{"messages": [{"role": "assistant", "content": "x"}, {"role": "user", "content": "y"}]}])
        self.assertTrue(any("assistant reply" in e for e in errors))

    def test_empty_reply_is_an_error(self):
        errors, _ = check_data.check_rows("train", [self._row("q", "  ")])
        self.assertTrue(any("empty" in e for e in errors))


class StyleCheck(unittest.TestCase):
    GOOD = "Hi Priya,\nWe're closed on Sundays and Mondays. Come Tuesday.\nCrumbs and kindness, Maya at Bluebird Bakery"

    def test_good_reply_passes_everything(self):
        results = style_check.check_reply(CARD, self.GOOD)
        self.assertTrue(all(ok for ok, _ in results.values()), results)

    def test_missing_sign_off_and_greeting_fail(self):
        results = style_check.check_reply(CARD, "Dear customer, we are closed on Sunday.")
        self.assertFalse(results["sign_off"][0])
        self.assertFalse(results["greeting"][0])
        self.assertFalse(results["banned_phrases"][0])

    def test_too_long_and_dashes_fail(self):
        long_reply = "Hi Sam,\n" + " ".join(["Word."] * 70) + " \u2014 done\nCrumbs and kindness, Maya at Bluebird Bakery"
        results = style_check.check_reply(CARD, long_reply)
        self.assertFalse(results["length"][0])
        self.assertFalse(results["banned_characters"][0])

    def test_score_counts_full_passes(self):
        full, total, per = style_check.score(CARD, [self.GOOD, "no style at all"])
        self.assertEqual((full, total), (1, 2))
        self.assertEqual(per["sign_off"], 1)


class Honesty(unittest.TestCase):
    def test_honesty_counts_both_directions(self):
        replies = ["Let me check and come back to you today.", "We do deliver, tell me the address.",
                   "We open at 8am.", "I'll check with the baker."]
        kinds = ["unknown", "unknown", "normal", "normal"]
        ok_unknown, unknown_n, calm_normal, normal_n = style_check.honesty(CARD, replies, kinds)
        self.assertEqual((ok_unknown, unknown_n), (1, 2))   # one guessed
        self.assertEqual((calm_normal, normal_n), (1, 2))   # one said "check" when it should know

    def test_without_facts_keeps_only_the_role_line(self):
        messages = [{"role": "system", "content": "Role line.\nFacts: lots."}, {"role": "user", "content": "Hi"}]
        trimmed = compare.without_facts(messages)
        self.assertEqual(trimmed[0]["content"], "Role line.")
        self.assertEqual(trimmed[1], messages[1])


class TrainLogParsing(unittest.TestCase):
    # Real lines from an mlx-lm 0.32.2 run, including its colour codes.
    LOG = [
        "  \x1b[1miter   train_loss     tok/s     tokens\x1b[0m\n",
        "     1    \x1b[1;35mval\x1b[0m \x1b[1m3.076\x1b[0m    \x1b[38;5;244m4.03s\x1b[0m\n",
        "    10    \x1b[1;32m1.815 \u25bc\x1b[0m    \x1b[1m   28\x1b[0m    \x1b[38;5;244m  1.9k\x1b[0m\n",
        "    25    \x1b[1;35mval\x1b[0m \x1b[1m0.943\x1b[0m    \x1b[38;5;244m3.40s\x1b[0m\n",
        "    50    \x1b[1;35mval\x1b[0m \x1b[1m1.002\x1b[0m    \x1b[38;5;244m4.34s\x1b[0m\n",
        "   150    \x1b[1;32m0.001 \u25bc\x1b[0m    \x1b[1m   33\x1b[0m    \x1b[38;5;244m 29.4k\x1b[0m\n",
        "  4294967296  peak memory footprint\n",
    ]

    def test_numbers_are_extracted(self):
        parsed = train.parse_log(self.LOG)
        self.assertEqual(parsed["val_loss"], [(1, 3.076), (25, 0.943), (50, 1.002)])
        self.assertEqual(parsed["train_loss"], [(10, 1.815), (150, 0.001)])
        self.assertEqual(parsed["peak_memory_gb"], 4.0)

    def test_best_checkpoint_is_copied(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            (folder / "0000025_adapters.safetensors").write_bytes(b"best")
            (folder / "adapter_config.json").write_text("{}")
            best = train.keep_best_checkpoint(folder, 25)
            self.assertEqual((Path(best) / "adapters.safetensors").read_bytes(), b"best")
            self.assertIsNone(train.keep_best_checkpoint(folder, 99))

    def test_command_uses_masking_and_the_given_settings(self):
        class Args:
            model = "m"; data = "d"; adapter_path = "a"; iters = 5; batch_size = 2
            num_layers = 8; learning_rate = 1e-5; max_seq_length = 512
            report_every = 1; eval_every = 5; save_every = 5; seed = 1; grad_checkpoint = True

        command = train.build_command(Args)
        self.assertIn("--mask-prompt", command)
        self.assertIn("--grad-checkpoint", command)
        self.assertEqual(command[command.index("--iters") + 1], "5")


class Fuse(unittest.TestCase):
    def test_fuse_always_dequantizes(self):
        command = fuse.build_command("m", "a", "s")
        self.assertIn("--dequantize", command)
        self.assertEqual(command[command.index("--save-path") + 1], "s")


class Common(unittest.TestCase):
    def test_split_reply(self):
        greeting, body, last = common.split_reply("Hi A,\nOne. Two.\nBye")
        self.assertEqual((greeting, body, last), ("Hi A,", "One. Two.", "Bye"))

    def test_bad_json_line_names_the_line(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "x.jsonl"
            path.write_text('{"a": 1}\nnot json\n', encoding="utf-8")
            with self.assertRaises(ValueError) as ctx:
                common.read_jsonl(path)
            self.assertIn("line 2", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
