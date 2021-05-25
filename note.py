import cv2

from config import NOTE_PITCH_DETECTION_MIDDLE_SNAPPING, VERBOSE
from hu import classify_clef
from util import distance

violin_key = {
    -6: 'C6',
    -5: 'D6',
    -4: 'C6',
    -3: 'H5',
    -2: 'A5',
    -1: 'G5',
    0:  'F5',
    1:  'E5',
    2:  'D5',
    3:  'C5',
    4:  'H4',
    5:  'A4',
    6:  'G4',
    7:  'F4',
    8:  'E4',
    9:  'D4',
    10: 'C4',
    11: 'H3',
    12: 'A3',
    13: 'G3',
    14: 'F3',
}

bass_key = {
    -6: 'G3',
    -5: 'F3',
    -4: 'E3',
    -3: 'D3',
    -2: 'C3',
    -1: 'H3',
    0:  'A3',
    1:  'G3',
    2:  'F3',
    3:  'E3',
    4:  'D3',
    5:  'C3',
    6:  'H2',
    7:  'A2',
    8:  'G2',
    9:  'F2',
    10: 'E2',
    11: 'D2',
    12: 'C2',
    13: 'H1',
    14: 'A1',
}

guitar_key = {
    -6: '-6',
    -5: '-5',
    -4: '-4',
    -3: 'B4',
    -2: 'A4',
    -1: 'G4',
    0:  'F4',
    1:  'E4',
    2:  'D4',
    3:  'C3',
    4:  'B3',
    5:  'A3',
    6:  'G3',
    7:  'F3',
    8:  'E3',
    9:  'D3',
    10: 'C3',
    11: 'B3',
    12: 'A3',
    13: 'G3',
    14: 'F3',
}

guitar_hand_key = {
    -6: 'e13',
    -5: 'e11',
    -4: 'e9',
    -3: 'e7',
    -2: 'e5',
    -1: 'e3',
    0:  'e1',
    1:  'e0',
    2:  'B3',
    3:  'B1',
    4:  'B0',
    5:  'G2',
    6:  'G0',
    7:  'D3',
    8:  'D2',
    9:  'D0',
    10: 'A3',
    11: 'A2',
    12: 'A0',
    13: 'E3',
    14: 'E1',
}


def extract_notes(blobs, staffs, image):
    clef = classify_clef(image, staffs[0])
    notes = []
    if VERBOSE:
        print('Detected clef: ' + clef)
        print('Extracting notes from blobs.')
    for blob in blobs:
        if blob[1] % 2 == 1:
            staff_no = int((blob[1] - 1) / 2)
            notes.append(Note(staff_no, staffs, blob[0], clef))
    if VERBOSE:
        print('Extracted ' + str(len(notes)) + ' notes.')
    return notes


def draw_notes_pitch(image, notes):
    im_with_pitch = image.copy()
    im_with_pitch = cv2.cvtColor(im_with_pitch, cv2.COLOR_GRAY2BGR)
    for note in notes:
        cv2.putText(im_with_pitch, note.pitch, (int(note.center[0]) - 5, int(note.center[1]) + 35),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=1.5, color=(255, 0, 0), thickness=3)
    cv2.imwrite("C:\\cip\\music\\music\\static\\media\\output\\9a_with_pitch.png", im_with_pitch)
    
def draw_notes_hand(image, notes):
    im_with_hand = image.copy()
    im_with_hand = cv2.cvtColor(im_with_hand, cv2.COLOR_GRAY2BGR)
    for note in notes:
        cv2.putText(im_with_hand, note.hand, (int(note.center[0]) - 5, int(note.center[1]) + 35),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=1.5, color=(0, 0, 255), thickness=4)
    cv2.imwrite("C:\\cip\\music\\music\\static\\media\\output\\9b_with_hand.png", im_with_hand)



# noinspection PyMethodMayBeStatic
class Note:
    """
    Represents a single note
    """
    def __init__(self, staff_no, staffs, blob, clef):
        self.position_on_staff = self.detect_position_on_staff(staffs[staff_no], blob)
        self.staff_no = staff_no
        self.center = blob.pt
        self.clef = clef
        self.pitch = self.detect_pitch(self.position_on_staff)
        self.hand = self.detect_hand(self.position_on_staff)

    def detect_position_on_staff(self, staff, blob):
        distances_from_lines = []
        x, y = blob.pt
        for line_no, line in enumerate(staff.lines_location):
            distances_from_lines.append((2 * line_no, distance((x, y), (x, line))))
        # Generate three upper lines
        for line_no in range(5, 8):
            distances_from_lines.append((2 * line_no, distance((x, y), (x, staff.min_range + line_no * staff.lines_distance))))
        # Generate three lower lines
        for line_no in range(-3, 0):
            distances_from_lines.append((2 * line_no, distance((x, y), (x, staff.min_range + line_no * staff.lines_distance))))

        distances_from_lines = sorted(distances_from_lines, key=lambda tup: tup[1])
        # Check whether difference between two closest distances is within MIDDLE_SNAPPING value specified in config.py
        if distances_from_lines[1][1] - distances_from_lines[0][1] <= NOTE_PITCH_DETECTION_MIDDLE_SNAPPING:
            # Place the note between these two lines
            return int((distances_from_lines[0][0] + distances_from_lines[1][0]) / 2)
        else:
            # Place the note on the line closest to blob's center
            return distances_from_lines[0][0]

   # def send_instrument(instrument):
    #    if instrument == 'guitar':
     #       return myinstru == 'guitar'
      #  else:
       #     return myinstru == 'violin'

    #def get_instrument():
     #   return send_instrument

    def detect_pitch(self, position_on_staff):
        instrument = 'guitar'          #if self.clef == 'violin':
        if instrument == 'guitar': 
            return guitar_key[position_on_staff] #return violin_key[position_on_staff]
        elif instrument == 'violin':
            return violin_key[position_on_staff]
        else: 
            return bass_key[position_on_staff]

    def detect_hand(self, position_on_staff):
        instrument = 'guitar'  #if self.clef == 'violin':
        if instrument == 'guitar': 
            return guitar_hand_key[position_on_staff] #return violin_key[position_on_staff]
        else:
             return bass_key[position_on_staff]
