import numpy as np

def decode_seat(seat):
    row, col = seat[:7], seat[7:]
    row = int('0b' + ''.join('1' if s == 'b' else '0' for s in row.lower()), base=2)
    col = int('0b' + ''.join('1' if s == 'r' else '0' for s in col.lower()), base=2)
    return row, col, row * 8 + col

def main():
    with open("../input/05.txt") as f:
        lines = [l.strip() for l in f.readlines()]
    seats = [
        'BFFFBBFRRR',
        'FFFBBBFRRR',
        'BBFFBBFRLL',
    ]
    print(list(map(decode_seat, seats)))
    print(list(map(decode_seat, lines)))
    ids = list(decode_seat(s)[2] for s in lines)
    print(max(ids))
    ids.sort()
    ids = np.array(ids)
    print(ids[:-1][np.diff(ids) == 2] + 1)
    

if __name__ == "__main__":
    main()
