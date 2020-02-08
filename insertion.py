#!/usr/bin/env python
# -*- coding: utf-8 -*-

from manimlib.imports import *

SCALE = 1.2


class Element:
    def __init__(self, val):
        self.val = val
        self.circle = Circle(radius=0.4 * SCALE)
        self.text = TextMobject(str(self.val))
        self.text.scale(SCALE)


def move_el(el, direction):
    return [
        ApplyMethod(el.circle.shift, direction * SCALE),
        ApplyMethod(el.text.shift, direction * SCALE)
    ]


class InsertionSort(Scene):
    def construct(self):
        arr = [0, 7, 3, 5, 2, 4, 8]
        els = [Element(i) for i in arr]

        # Move elements to the right positions
        bias = (len(arr) - 1) / 2
        for i in range(len(arr)):
            new_pos = [(-bias + i) * SCALE, 0, 0]
            els[i].circle.move_to(new_pos)
            els[i].text.move_to(new_pos)

        # Show elements
        self.play(*[ShowCreation(el.circle) for el in els],
                  *[Write(el.text) for el in els])

        # Insertion sort
        self.play(ApplyMethod(els[0].circle.set_color, BLUE_C))
        for i in range(1, len(arr)):
            # Show current processing element
            selected_el = els[i]
            self.play(*move_el(selected_el, UP))
            j = i - 1
            while j >= 0 and els[j].val > selected_el.val:
                els[j + 1] = els[j]
                self.play(*move_el(els[j], RIGHT))
                j -= 1

            # Move selected element to right position
            els[j + 1] = selected_el
            self.play(*move_el(selected_el, LEFT * (i - j - 1)))
            self.play(*move_el(selected_el, DOWN))

            # Mark (j+1)th element as finished
            self.play(ApplyMethod(els[j + 1].circle.set_color, BLUE_C))

        # Finished!
        self.wait(3)
