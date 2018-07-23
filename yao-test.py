import unittest
import random
from b64utils import *
from fastpow import *
from fastSerialize import *
from millionare import RandomNumbers, \
    role_a_generator, role_b_generator, score_limit, \
    role_a, role_b

def randint():
    return random.randint(0, 23333333)

class TestB64Utils(unittest.TestCase):
    def test_encode_decode(self):
        for i in range(1, 10000):
            n = random.getrandbits(i)
            self.assertEqual(n, int_b64decode(int_b64encode(n)))
        self.assertEqual('VVVVVQ==', int_b64encode(0x55555555))  # b'UUUU'
        self.assertEqual(0x55555555, int_b64decode('VVVVVQ=='))

    def test_fast_pow(self):
        for k in range(12):
            for i in range(64):
                for j in [23333, 2000, 32768]:
                    self.assertEqual(k ** i % j, pow(k, i, j))

    def test_serialize(self):
        for i in range(1, 10):
            l = list(range(i * 1000))
            self.assertEqual(l, fast_load(fast_dump(l)))

        l = list(range(100))
        with self.assertRaises(AssertionError):
            fast_load(fast_dump(l) + '$')

    def test_main_randomlist(self):
        a = list(range(21))
        a.append(-1)
        rn1 = RandomNumbers(list(range(21)), -1)
        self.assertEqual(a, rn1.to_list())

        rn2 = RandomNumbers.from_list(a)
        self.assertEqual(rn2.l, list(range(21)))
        self.assertEqual(rn2.p, -1)

    def test_main_generators(self):
        possible = score_limit['up'] - score_limit['low']

        def testing(a_score, b_score):
            B = role_b_generator(b_score)
            pub_key = B.send(None)
            A = role_a_generator(a_score, pub_key)
            cipher_score = A.send(None)
            mod_list = B.send(cipher_score)
            result = A.send(mod_list)

            if a_score < b_score:
                expect_result = '<partner'
            else:
                expect_result = '>=partner'

            self.assertEqual(result, expect_result)

        for _ in range(3):
            a_score, b_score = random.sample(range(possible + 1), 2)
            testing(a_score, b_score)
            testing(b_score, a_score)

        for i in [0, 1, 2]:
            testing(i, i)

        for i in range(possible - 2, possible + 1):
            testing(i, i)

if __name__ == '__main__':
    unittest.main()
