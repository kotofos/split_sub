from split.split_subs import process_srt


def test_srt_simple_split():
    text = (
        '1\n'
        '00:02:17,440 --> 00:02:20,375\n'
        'a: Senator, we\'re making\n'
        'our final approach into Coruscant.\n'
        '\n'
        '2\n'
        '00:02:20,476 --> 00:02:22,501\n'
        'b: Very good, Lieutenant.\n'
    )

    res = process_srt(text)
    expected = [
        ('02:17', 'a',
         'Senator, we\'re making our final approach into Coruscant.'),
        ('02:20', 'b', 'Very good, Lieutenant.')
    ]
    assert res == expected


def test_srt_two_chars_split():
    text = (
        '1\n'
        '00:02:17,440 --> 00:02:20,375\n'
        'a: a line\n'
        'b: b line\n'
        '\n'
        '2\n'
        '00:02:20,476 --> 00:02:22,501\n'
        'b: 2nd b line\n'
        'c: c line.\n'
    )

    res = process_srt(text)

    expected = [
        ('02:17', 'a',
         'a line'),
        ('02:17', 'b',
         'b line'),
        ('02:20', 'b', '2nd b line'),
        ('02:20', 'c', 'c line.')
    ]
    assert res == expected


def test_srt_continuation_chars_split():
    text = (
        '1\n'
        '00:02:17,440 --> 00:02:20,375\n'
        'a: a line\n'
        '2a line\n'
        '\n'
        '2\n'
        '00:02:20,476 --> 00:02:22,501\n'
        '3a line.\n'
    )

    res = process_srt(text)
    expected = [
        ('02:17', 'a', 'a line 2a line 3a line.'),
    ]
    assert res == expected
