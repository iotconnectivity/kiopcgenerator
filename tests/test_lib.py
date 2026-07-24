import unittest

import kiopcgenerator

# Known vector taken from the README usage example.
OP = "D7DECB1F50404CC29ECBF989FE73AFC5"
TRANSPORT = "2257CC6E9746434B89F346F0276CCAEC"
KI = "780E6AC95A2E43449C15BDCDD0450982"
OPC = "2274B84B8043105A28AABBE53EF1D014"
EKI = "4601138387FCF7D666ED24BBB3EE37B8"


class GenOpcTest(unittest.TestCase):
    def test_known_vector(self):
        self.assertEqual(kiopcgenerator.gen_opc(OP, KI), OPC)

    def test_invalid_hex_raises(self):
        with self.assertRaises(ValueError):
            kiopcgenerator.gen_opc("ZZ", KI)

    def test_invalid_key_length_raises(self):
        with self.assertRaises(ValueError):
            kiopcgenerator.gen_opc(OP, "AABB")


class GenEkiTest(unittest.TestCase):
    def test_known_vector(self):
        self.assertEqual(kiopcgenerator.gen_eki(TRANSPORT, KI), EKI)

    def test_invalid_ki_hex_raises(self):
        with self.assertRaises(ValueError):
            kiopcgenerator.gen_eki(TRANSPORT, "ZZ")

    def test_invalid_ki_length_raises(self):
        with self.assertRaises(ValueError):
            kiopcgenerator.gen_eki(TRANSPORT, "AABB")

    def test_invalid_transport_hex_raises(self):
        with self.assertRaises(ValueError):
            kiopcgenerator.gen_eki("ZZ", KI)

    def test_invalid_transport_length_raises(self):
        with self.assertRaises(ValueError):
            kiopcgenerator.gen_eki("AABB", KI)


class RecoverKiTest(unittest.TestCase):
    def test_known_vector(self):
        self.assertEqual(
            kiopcgenerator.recover_ki(OP, TRANSPORT, EKI),
            {"KI": KI, "OPC": OPC, "eKI": EKI},
        )

    def test_round_trip_with_random_ki(self):
        ki = kiopcgenerator.gen_ki()
        eki = kiopcgenerator.gen_eki(TRANSPORT, ki)
        recovered = kiopcgenerator.recover_ki(OP, TRANSPORT, eki)
        self.assertEqual(recovered["KI"], ki)
        self.assertEqual(recovered["OPC"], kiopcgenerator.gen_opc(OP, ki))

    def test_invalid_eki_hex_raises(self):
        with self.assertRaises(ValueError):
            kiopcgenerator.recover_ki(OP, TRANSPORT, "ZZ")

    def test_invalid_eki_length_raises(self):
        with self.assertRaises(ValueError):
            kiopcgenerator.recover_ki(OP, TRANSPORT, "AABB")

    def test_invalid_transport_hex_raises(self):
        with self.assertRaises(ValueError):
            kiopcgenerator.recover_ki(OP, "ZZ", EKI)

    def test_invalid_transport_length_raises(self):
        with self.assertRaises(ValueError):
            kiopcgenerator.recover_ki(OP, "AABB", EKI)

    def test_invalid_op_hex_raises(self):
        with self.assertRaises(ValueError):
            kiopcgenerator.recover_ki("ZZ", TRANSPORT, EKI)

    def test_invalid_op_length_raises(self):
        with self.assertRaises(ValueError):
            kiopcgenerator.recover_ki("AABB", TRANSPORT, EKI)


if __name__ == "__main__":
    unittest.main()
