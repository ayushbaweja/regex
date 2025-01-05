from thompson_construction import (
    single_char,
    any_char,
    zero_or_more,
    one_or_more,
    union,
    concat,
    optional,
)
from evaluator import Evaluator

def test_single_char():
    # Test pattern: 'a'
    pattern = single_char('a')
    evaluator = Evaluator(pattern)

    # Should match
    assert evaluator.match('a'), "Should match 'a'"

    # Should not match
    assert not evaluator.match(''), "Should not match empty string"
    assert not evaluator.match('b'), "Should not match 'b'"
    assert not evaluator.match('aa'), "Should not match 'aa'"

    print("All single_char tests passed!")

def test_any_char():
    # Test pattern: '.'
    pattern = any_char()
    evaluator = Evaluator(pattern)

    # Should match any single character
    assert evaluator.match('a'), "Should match 'a'"
    assert evaluator.match('b'), "Should match 'b'"
    assert evaluator.match('1'), "Should match '1'"

    # Should not match
    assert not evaluator.match(''), "Should not match empty string"
    assert not evaluator.match('aa'), "Should not match multiple chars"

    print("All any_char tests passed!")

def test_zero_or_more():
    # Test pattern: a*
    pattern = zero_or_more(single_char('a'))
    evaluator = Evaluator(pattern)

    # Should match
    assert evaluator.match(''), "Should match empty string"
    assert evaluator.match('a'), "Should match single 'a'"
    assert evaluator.match('aa'), "Should match 'aa'"
    assert evaluator.match('aaa'), "Should match 'aaa'"

    # Should not match
    assert not evaluator.match('b'), "Should not match 'b'"
    assert not evaluator.match('ab'), "Should not match 'ab'"

    print("All zero_or_more tests passed!")

def test_one_or_more():
    # Test pattern: a+
    pattern = one_or_more(single_char('a'))
    evaluator = Evaluator(pattern)

    # Should match
    assert evaluator.match('a'), "Should match single 'a'"
    assert evaluator.match('aa'), "Should match 'aa'"
    assert evaluator.match('aaa'), "Should match 'aaa'"

    # Should not match
    assert not evaluator.match(''), "Should not match empty string"
    assert not evaluator.match('b'), "Should not match 'b'"
    assert not evaluator.match('ab'), "Should not match 'ab'"

    print("All one_or_more tests passed!")

def test_union():
    # Test pattern: a|b (matches either 'a' or 'b')
    pattern = union(single_char('a'), single_char('b'))
    evaluator = Evaluator(pattern)

    # Should match
    assert evaluator.match('a'), "Should match 'a'"
    assert evaluator.match('b'), "Should match 'b'"

    # Should not match
    assert not evaluator.match(''), "Should not match empty string"
    assert not evaluator.match('c'), "Should not match 'c'"
    assert not evaluator.match('ab'), "Should not match 'ab'"
    assert not evaluator.match('aa'), "Should not match 'aa'"
    assert not evaluator.match('bb'), "Should not match 'bb'"

    print("All union tests passed!")

def test_union_complex():
    # Test pattern: (ab)|(cd) (matches either "ab" or "cd")
    left = concat(single_char('a'), single_char('b'))
    right = concat(single_char('c'), single_char('d'))
    pattern = union(left, right)
    evaluator = Evaluator(pattern)

    # Should match
    assert evaluator.match('ab'), "Should match 'ab'"
    assert evaluator.match('cd'), "Should match 'cd'"

    # Should not match
    assert not evaluator.match(''), "Should not match empty string"
    assert not evaluator.match('a'), "Should not match 'a'"
    assert not evaluator.match('b'), "Should not match 'b'"
    assert not evaluator.match('c'), "Should not match 'c'"
    assert not evaluator.match('d'), "Should not match 'd'"
    assert not evaluator.match('ac'), "Should not match 'ac'"
    assert not evaluator.match('bd'), "Should not match 'bd'"
    assert not evaluator.match('abcd'), "Should not match 'abcd'"

    print("All complex union tests passed!")

def test_optional():
    # Test pattern: a? (matches '' or 'a')
    pattern = optional(single_char('a'))
    evaluator = Evaluator(pattern)

    # Should match
    assert evaluator.match(''), "Should match empty string"
    assert evaluator.match('a'), "Should match 'a'"

    # Should not match
    assert not evaluator.match('b'), "Should not match 'b'"
    assert not evaluator.match('aa'), "Should not match 'aa'"
    assert not evaluator.match('ab'), "Should not match 'ab'"

    print("All optional tests passed!")

if __name__ == "__main__":
    test_single_char()
    test_any_char()
    test_zero_or_more()
    test_one_or_more()
    test_union()
    test_union_complex()
    test_optional()
