import unittest
import binascii
import bip66
import json
import re

fixtures_json = """
{
  "valid": [
    {
      "DER": "3044022029db2d5f4e1dcc04e19266cce3cb135865784c62ab653b307f0e0bb744f5c2aa022000a97f5826912cac8b44d9f577a26f169a2f8db781f2ddb7de2bc886e93b6844",
      "r": "29db2d5f4e1dcc04e19266cce3cb135865784c62ab653b307f0e0bb744f5c2aa",
      "s": "00a97f5826912cac8b44d9f577a26f169a2f8db781f2ddb7de2bc886e93b6844"
    },
    {
      "DER": "304302201ea1fdff81b3a271659df4aad19bc4ef83def389131a36358fe64b245632e777021f29e164658be9ce810921bf81d6b86694785a79ea1e52dbfa5105148d1f0bc1",
      "r": "1ea1fdff81b3a271659df4aad19bc4ef83def389131a36358fe64b245632e777",
      "s": "29e164658be9ce810921bf81d6b86694785a79ea1e52dbfa5105148d1f0bc1"
    },
    {
      "DER": "304402201b19519b38ca1e6813cd25649ad36be8bc6a6f2ad9758089c429acd9ce0b572f02203bf32193c8a3a3de1f847cd6e6eebf43c96df1ffa4d7fe920f8f71708920c65f",
      "r": "1b19519b38ca1e6813cd25649ad36be8bc6a6f2ad9758089c429acd9ce0b572f",
      "s": "3bf32193c8a3a3de1f847cd6e6eebf43c96df1ffa4d7fe920f8f71708920c65f"
    },
    {
      "DER": "3044022000c8da1836747d05a6a3d2c395825edce827147d15909e66939a5037d5916e6f022017823c2da62f539d7f8e1e186eaea7a401ab3c077dcfc44aeaf3e13fac99bdbc",
      "r": "00c8da1836747d05a6a3d2c395825edce827147d15909e66939a5037d5916e6f",
      "s": "17823c2da62f539d7f8e1e186eaea7a401ab3c077dcfc44aeaf3e13fac99bdbc"
    },
    {
      "DER": "3042021e2ff2609c8dc0392d3731a2c6312841e09c76f10b83e2b52604dc84886dd502200090ac80e787c063618192bc04758e6666d0179c377fb2f3d6105d58000f33ac",
      "r": "2ff2609c8dc0392d3731a2c6312841e09c76f10b83e2b52604dc84886dd5",
      "s": "0090ac80e787c063618192bc04758e6666d0179c377fb2f3d6105d58000f33ac"
    },
    {
      "DER": "3041021d00feb1a12c27e5fe261acc64c0923add082573883e0800d8e4080fa9bb02202e7aeb97f4046ea3be60d2896a19c8dc269ab5eb2de968912cd52a076a0a42e9",
      "r": "00feb1a12c27e5fe261acc64c0923add082573883e0800d8e4080fa9bb",
      "s": "2e7aeb97f4046ea3be60d2896a19c8dc269ab5eb2de968912cd52a076a0a42e9"
    },
    {
      "DER": "3042021d00feb1a12c27e5fe261acc64c0923add082573883e0800d8e4080fa9bb0221008aeb97f4046ea3be60d2896a19c8dc269ab5eb2de968912cd52a076a0a42e925",
      "r": "00feb1a12c27e5fe261acc64c0923add082573883e0800d8e4080fa9bb",
      "s": "008aeb97f4046ea3be60d2896a19c8dc269ab5eb2de968912cd52a076a0a42e925"
    },
    {
      "DER": "303e021d00c1d545da2e4edfbc65e9267d3c0a6fdda41793d0fd945f15acbcf0dd021d009acffda3ca5e7c349c35ba606f0a8f1ec7815b653b51695ca9ee69a6",
      "r": "00c1d545da2e4edfbc65e9267d3c0a6fdda41793d0fd945f15acbcf0dd",
      "s": "009acffda3ca5e7c349c35ba606f0a8f1ec7815b653b51695ca9ee69a6"
    },
    {
      "DER": "3006020100020100",
      "r": "00",
      "s": "00"
    }
  ],
  "invalid": {
    "encode": [
      {
        "exception": "^Error: R length is zero$",
        "r": "",
        "s": "0080000000000000000000000000000000000000000000000000000000000000"
      },
      {
        "exception": "^Error: S length is zero$",
        "r": "0080000000000000000000000000000000000000000000000000000000000000",
        "s": ""
      },
      {
        "exception": "^Error: R value is negative$",
        "r": "80",
        "s": "7f"
      },
      {
        "exception": "^Error: S value is negative$",
        "r": "7f",
        "s": "80"
      },
      {
        "exception": "^Error: R value excessively padded$",
        "r": "0010000000000000000000000000000000000000000000000000000000000000",
        "s": "0080000000000000000000000000000000000000000000000000000000000000"
      },
      {
        "exception": "^Error: S value excessively padded$",
        "r": "0080000000000000000000000000000000000000000000000000000000000000",
        "s": "0010000000000000000000000000000000000000000000000000000000000000"
      },
      {
        "exception": "^Error: R length is too long$",
        "r": "00800000000000000000000000000000000000000000000000000000000000000000",
        "s": "008000000000000000000000000000000000000000000000000000000000000000"
      },
      {
        "exception": "^Error: S length is too long$",
        "r": "008000000000000000000000000000000000000000000000000000000000000000",
        "s": "00800000000000000000000000000000000000000000000000000000000000000000"
      }
    ],
    "decode": [
      {
        "exception": "^Error: DER sequence length is too short$",
        "DER": "ffffffffffffff"
      },
      {
        "exception": "^Error: DER sequence length is too long$",
        "DER": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
      },
      {
        "exception": "^Error: Expected DER sequence$",
        "DER": "00ffff0400ffffff020400ffffff"
      },
      {
        "exception": "^Error: DER sequence length is invalid$",
        "DER": "30ff020400ffffff020400ffffff"
      },
      {
        "exception": "^Error: DER sequence length is invalid$",
        "DER": "300c030400ffffff030400ffffff0000"
      },
      {
        "exception": "^Error: Expected DER integer$",
        "DER": "300cff0400ffffff020400ffffff"
      },
      {
        "exception": "^Error: Expected DER integer \\\\(2\\\\)$",
        "DER": "300c020200ffffff020400ffffff"
      },
      {
        "exception": "^Error: R length is zero$",
        "DER": "30080200020400ffffff"
      },
      {
        "exception": "^Error: S length is zero$",
        "DER": "3008020400ffffff0200"
      },
      {
        "exception": "^Error: R length is too long$",
        "DER": "300c02dd00ffffff020400ffffff"
      },
      {
        "exception": "^Error: S length is invalid$",
        "DER": "300c020400ffffff02dd00ffffff"
      },
      {
        "exception": "^Error: R value is negative$",
        "DER": "300c020480000000020400ffffff"
      },
      {
        "exception": "^Error: S value is negative$",
        "DER": "300c020400ffffff020480000000"
      },
      {
        "exception": "^Error: R value excessively padded$",
        "DER": "300c02040000ffff020400ffffff"
      },
      {
        "exception": "^Error: S value excessively padded$",
        "DER": "300c020400ffffff02040000ffff"
      }
    ]
  }
}
"""


fixtures = json.loads(fixtures_json)


class TestBip66(unittest.TestCase):

    DER = "3044022029db2d5f4e1dcc04e19266cce3cb135865784c62ab653b307f0e0bb" \
          "744f5c2aa022000a97f5826912cac8b44d9f577a26f169a2f8db781f2ddb7de2bc886e93b6844"
    r = "29db2d5f4e1dcc04e19266cce3cb135865784c62ab653b307f0e0bb744f5c2aa"
    s = "00a97f5826912cac8b44d9f577a26f169a2f8db781f2ddb7de2bc886e93b6844"

    def test_bip66_encode(self):
        encoded = bip66.encode(binascii.unhexlify(self.r), binascii.unhexlify(self.s))
        signature = binascii.hexlify(encoded).decode()
        self.assertEqual(signature, self.DER)

    def test_bip66_decode(self):
        r, s = bip66.decode(binascii.unhexlify(self.DER))
        self.assertEqual(self.r, binascii.hexlify(r).decode())
        self.assertEqual(self.s, binascii.hexlify(s).decode())


class TestSequence(unittest.TestCase):
    pass


def test_check_generator(DER):
    def test(self):
        self.assertEqual(bip66.check(binascii.unhexlify(DER)), True)
    return test


def test_decode_generator(DER, r, s):
    def test(self):
        r_, s_ = bip66.decode(binascii.unhexlify(DER))
        self.assertEqual(r, binascii.hexlify(r_).decode())
        self.assertEqual(s, binascii.hexlify(s_).decode())
    return test


def test_encode_generator(DER, r, s):
    def test(self):
        encoded = bip66.encode(binascii.unhexlify(r), binascii.unhexlify(s))
        signature = binascii.hexlify(encoded).decode()
        self.assertEqual(signature, DER)
    return test


def test_decode_exception_generator(DER, exception):
    def test(self):
        pattern = re.compile(exception)
        try:
            bip66.decode(binascii.unhexlify(DER))
        except bip66.Bip66Error as context:\
            self.assertNotEqual(pattern.match('Error: ' + str(context)), None)
    return test


def test_check_invalid_generator(DER):
    def test(self):
        self.assertEqual(bip66.check(binascii.unhexlify(DER)), False)
    return test


def test_encode_exception_generator(r, s, exception):
    def test(self):
        pattern = re.compile(exception)
        try:
            bip66.encode(binascii.unhexlify(r), binascii.unhexlify(s))
        except bip66.Bip66Error as context:\
            self.assertNotEqual(pattern.match('Error: ' + str(context)), None)
    return test


for fix in fixtures['valid']:
    test_name_check = 'test_check_returns_true_for_' + fix['DER']
    test_check = test_check_generator(fix['DER'])
    setattr(TestSequence, test_name_check, test_check)

    test_name_decode = 'test_decode_' + fix['DER']
    test_decode = test_decode_generator(fix['DER'], fix['r'], fix['s'])
    setattr(TestSequence, test_name_decode, test_decode)

    test_name_encode = 'test_encode_' + fix['r'] + '_' + fix['s']
    test_encode = test_encode_generator(fix['DER'], fix['r'], fix['s'])
    setattr(TestSequence, test_name_encode, test_encode)

for fix in fixtures['invalid']['decode']:
    test_name_decode = 'test_raises_' + fix['exception'] + '_for_' + fix['DER']
    test_decode = test_decode_exception_generator(fix['DER'], fix['exception'])
    setattr(TestSequence, test_name_decode, test_decode)

    test_name_check = 'test_check_returns_false_for_' + fix['DER']
    test_check = test_check_invalid_generator(fix['DER'])
    setattr(TestSequence, test_name_check, test_check)

for fix in fixtures['invalid']['encode']:
    test_name_encode = 'test_raises_' + fix['exception'] + '_for_' + fix['r'] + '_' + fix['s']
    test_encode = test_encode_exception_generator(fix['r'], fix['s'], fix['exception'])
    setattr(TestSequence, test_name_encode, test_encode)

if __name__ == '__main__':
    unittest.main()

