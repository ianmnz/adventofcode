# Advent of Code : Day 06 - Tuning Trouble
# https://adventofcode.com/2022/day/6


def main() -> None:
    buffer = ''

    start_of_packet_marker_idx = 0
    start_of_packet_marker_length = 4
    start_of_packet_marker = ''

    start_of_message_marker_idx = 0
    start_of_message_marker_length = 14
    start_of_message_marker = ''

    with open('input.txt', 'r') as file:
        for line in file:
            buffer += line

    found_packet = False
    found_message = False

    # We assume that start_of_packet_marker_length < start_of_message_marker_length
    for idx in range(start_of_packet_marker_length - 1, len(buffer)):

        subbuffer_packet = \
            buffer[idx - (start_of_packet_marker_length - 1) : idx + 1]

        if (not found_packet) and \
            (len(set(subbuffer_packet)) == start_of_packet_marker_length):
            start_of_packet_marker_idx = idx + 1
            start_of_packet_marker = subbuffer_packet
            found_packet = True

        if idx < (start_of_message_marker_length - 1):
            continue

        subbuffer_message = \
            buffer[idx - (start_of_message_marker_length - 1) : idx + 1]

        if (not found_message) and \
            (len(set(subbuffer_message)) == start_of_message_marker_length):
            start_of_message_marker_idx = idx + 1
            start_of_message_marker = subbuffer_message
            found_message = True

        if found_packet and found_message:
            break

    # Answer part 1 :
    print(f'Start-of-packet marker index: {start_of_packet_marker_idx}') # 1833
    print(f'Start-of-packet marker: {start_of_packet_marker}') # wbcl

    # Answer part 2 :
    print(f'Start-of-message marker index: {start_of_message_marker_idx}') # 3425
    print(f'Start-of-message marker: {start_of_message_marker}') # vbnwqdhtlsfcjz


if __name__ == "__main__":
    main()