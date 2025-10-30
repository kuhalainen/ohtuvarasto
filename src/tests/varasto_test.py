import unittest
from varasto import Varasto


class TestVarasto(unittest.TestCase):
    def setUp(self):
        self.varasto = Varasto(10)

    def test_konstruktori_luo_tyhjan_varaston(self):
        # https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertAlmostEqual
        self.assertAlmostEqual(self.varasto.saldo, 0)

    def test_uudella_varastolla_oikea_tilavuus(self):
        self.assertAlmostEqual(self.varasto.tilavuus, 10)

    def test_lisays_lisaa_saldoa(self):
        self.varasto.lisaa_varastoon(8)

        self.assertAlmostEqual(self.varasto.saldo, 8)

    def test_lisays_lisaa_pienentaa_vapaata_tilaa(self):
        self.varasto.lisaa_varastoon(8)

        # vapaata tilaa pitäisi vielä olla tilavuus-lisättävä määrä eli 2
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 2)

    def test_ottaminen_palauttaa_oikean_maaran(self):
        self.varasto.lisaa_varastoon(8)

        saatu_maara = self.varasto.ota_varastosta(2)

        self.assertAlmostEqual(saatu_maara, 2)

    def test_ottaminen_lisaa_tilaa(self):
        self.varasto.lisaa_varastoon(8)

        self.varasto.ota_varastosta(2)

        # varastossa pitäisi olla tilaa 10 - 8 + 2 eli 4
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 4)

###############################################

    def test_uudella_negatiivinen_saldo(self):
        storage = Varasto(2,-1)
        self.assertAlmostEqual(storage.saldo, 0)

    def test_uudella_varastolla_tilasto_nollaus(self):
        varasto = Varasto(-1)
        self.assertAlmostEqual(varasto.tilavuus, 0)

    def test_uudella_varastolla_ei_mahdu(self):
        storage = Varasto(3,20)
        self.assertAlmostEqual(storage.saldo, 3)

    def test_lisays_alle_nolla(self):
        saldooo = self.varasto.saldo
        self.varasto.lisaa_varastoon(-1)
        self.assertAlmostEqual(self.varasto.saldo, saldooo)

    def test_lisays_yli_tilavuuden(self):
        self.varasto.lisaa_varastoon(self.varasto.tilavuus + 2)
        self.assertAlmostEqual(self.varasto.saldo, self.varasto.tilavuus)

    def test_ota_tyhja(self):
        self.assertAlmostEqual(self.varasto.ota_varastosta(-4), 0)

    def test_ota_liikaa(self):
        kaikki = self.varasto.saldo
        otto = self.varasto.ota_varastosta(self.varasto.saldo + 5)
        self.assertAlmostEqual(self.varasto.saldo, 0)
        self.assertAlmostEqual(kaikki, otto)

    def test_printti(self):
        self.assertAlmostEqual(str(self.varasto), f"saldo = 0, vielä tilaa 10")