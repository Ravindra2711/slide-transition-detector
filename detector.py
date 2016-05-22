# -*- coding: utf-8 -*-

import argparse
import cv2
import imgcomparison
import timeline
import mediaoutput
import ui


class InfiniteCounter(object):
    """
    InfiniteCounter is a class that represents a counter that will
    return the next number indefinitely. When the user calls count()
    return the current number. Then it will increment the current
    number by the specified steps.
    """

    def __init__(self, start=0, step=1):
        """
        Default Initializer
        :param start: the starting value of the counter
        :param step: the amount that should be added at each step
        """
        self.current = start
        self.step = step

    def increment(self):
        self.current += self.step

    def count(self):
        """
        The count method yields the current number and then
        increments the current number by the specified step in the
        default initializer
        :return: the successor from the previous number
        """
        while True:
            yield self.current
            self.current += self.step


class Detector(object):

    def __init__(self, device, outpath, fileformat):
        cap = cv2.VideoCapture(sanitize_device(device))
        self.sequence = timeline.Timeline(cap)
        self.outpath = outpath
        self.fileformat = fileformat


    def detect_slides(self):
        slide_writer = mediaoutput.TimestampImageWriter(self.sequence.fps, self.outpath, self.fileformat)

        comparator = imgcomparison.AbsDiffHistComparator(0.99)

        progress = ui.ProgressController('Analyzing Video: ', self.sequence.len)
        progress.start()

        for i in self.analyze(comparator, slide_writer):
            progress.update(i)

        progress.finish()

        self.sequence.release_stream()

    def analyze(self, comparator, writer):
        prev_frame = self.sequence.next_frame()
        writer.write(prev_frame, 0)

        frame_counter = InfiniteCounter()
        for frame_count in frame_counter.count():

            frame = self.sequence.next_frame()

            if frame is None:
                break
            elif not comparator.are_same(prev_frame, frame):

                while True:
                    if comparator.are_same(prev_frame, frame):
                        break
                    prev_frame = frame
                    frame = self.sequence.next_frame()
                    frame_counter.increment()
                writer.write(frame, frame_count)

            prev_frame = frame

            yield frame_count


def sanitize_device(device):
    """returns device id if device can be converted to an integer"""
    try:
        return int(device)
    except (TypeError, ValueError):
        return device


if __name__ == "__main__":
    Parser = argparse.ArgumentParser(description="Slide Detector")
    Parser.add_argument("-d", "--device", help="video device number or path to video file")
    Parser.add_argument("-o", "--outpath", help="path to output video file", default="slides/", nargs='?')
    Parser.add_argument("-f", "--fileformat", help="file format of the output images e.g. '.jpg'",
                        default=".jpg", nargs='?')
    Args = Parser.parse_args()

    detector = Detector(Args.device, Args.outpath, Args.fileformat)
    detector.detect_slides()