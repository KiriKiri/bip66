Strict DER signature encoding/decoding.
-
[![PyPI version](https://badge.fury.io/py/bip66.svg)](https://badge.fury.io/py/bip66)

Installation
-
```bash
pip install bip66
```

This library is a migration of https://github.com/bitcoinjs/bip66 to python
-

See [bip66](https://github.com/bitcoin/bips/blob/master/bip-0066.mediawiki).

- This module **works only with [two's complement](https://en.wikipedia.org/wiki/Two's_complement) numbers**.
- BIP66 doesn't check that `r` or `s` are fully valid.
  - `check`/`decode` doesn't check that `r` or `s` great than 33 bytes or that this number represent valid point on elliptic curve.
  - `encode` doesn't check that `r`/`s` represent valid point on elliptic curve.

## Example

``` python
import binascii
import bip66
r = "29db2d5f4e1dcc04e19266cce3cb135865784c62ab653b307f0e0bb744f5c2aa"
s = "00a97f5826912cac8b44d9f577a26f169a2f8db781f2ddb7de2bc886e93b6844"
encoded = bip66.encode(binascii.unhexlify(r), binascii.unhexlify(s))
signature = binascii.hexlify(encoded).decode()
# > 3044022029db2d5f4e1dcc04e19266cce3cb135865784c62ab653b307f0e0bb744f5c2aa022000a97f5826912cac8b44d9f577a26f169a2f8db781f2ddb7de2bc886e93b6844

DER = "3044022029db2d5f4e1dcc04e19266cce3cb135865784c62ab653b307f0e0bb" \
      "744f5c2aa022000a97f5826912cac8b44d9f577a26f169a2f8db781f2ddb7de2bc886e93b6844"
r, s = bip66.decode(binascii.unhexlify(DER))
print(binascii.hexlify(r).decode())
print(binascii.hexlify(s).decode())

# > 29db2d5f4e1dcc04e19266cce3cb135865784c62ab653b307f0e0bb744f5c2aa
# > 00a97f5826912cac8b44d9f577a26f169a2f8db781f2ddb7de2bc886e93b6844
```

A catch-all exception regex:
``` python
/Expected DER (integer|sequence)|(R|S) value (excessively padded|is negative)|(R|S|DER sequence) length is (zero|too short|too long|invalid)/
```

## LICENSE [MIT](LICENSE)
