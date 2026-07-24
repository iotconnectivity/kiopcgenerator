import ast
import subprocess
import sys
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "kiopcgen"

# Known vector taken from the README usage example.
OP = "D7DECB1F50404CC29ECBF989FE73AFC5"
TRANSPORT = "2257CC6E9746434B89F346F0276CCAEC"
KI = "780E6AC95A2E43449C15BDCDD0450982"
OPC = "2274B84B8043105A28AABBE53EF1D014"
EKI = "4601138387FCF7D666ED24BBB3EE37B8"


class RecoverKiCliTest(unittest.TestCase):
    def test_recovers_ki_from_eki(self):
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "-o", OP,
                "-t", TRANSPORT,
                "-e", EKI,
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertEqual(
            ast.literal_eval(result.stdout),
            {"KI": KI, "OPC": OPC, "eKI": EKI},
        )


if __name__ == "__main__":
    unittest.main()
