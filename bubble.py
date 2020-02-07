#!/usr/bin/env python
# -*- coding: utf-8 -*-

from manimlib.imports import *
from copy import deepcopy

SCALE = 1.2


class Element:
    def __init__(self, val):
        self.val = val
        self.circle = Circle(radius=0.4 * SCALE)
        self.text = TextMobject(str(self.val))
        self.text.scale(SCALE)


def swap_mobjects(x1: Mobject, x2: Mobject):
    x1_copy, x2_copy = deepcopy(x1), deepcopy(x2)
    x1_copy.move_to(x2.get_center())
    x2_copy.move_to(x1.get_center())
    return [CounterclockwiseTransform(x1, x1_copy), CounterclockwiseTransform(x2, x2_copy)]


def swap_elements(e1: Element, e2: Element):
    return [*swap_mobjects(e1.text, e2.text), *swap_mobjects(e1.circle, e2.circle)]


class BubbleSort(Scene):
    def construct(self):
        arr = [0, 7, 3, 5, 2, 4, 8]
        els = [Element(i) for i in arr]

        # Create a sliding window
        rectangle = Rectangle(width=2 * SCALE, height=1 * SCALE)

        # Move elements to the right positions
        bias = (len(arr) - 1) / 2
        for i in range(len(arr)):
            new_pos = [(-bias + i) * SCALE, 0, 0]
            els[i].circle.move_to(new_pos)
            els[i].text.move_to(new_pos)

        # Show elements
        self.play(*[ShowCreation(el.circle) for el in els],
                  *[Write(el.text) for el in els])

        # Move rectangle to the right position
        rect_pos = midpoint(els[0].circle.get_center(), els[1].circle.get_center())
        rectangle.move_to(rect_pos)

        # Show rectangle
        self.play(ShowCreation(rectangle))

        # Bubble sort
        for i in range(len(arr)):
            flag = False
            for j in range(len(arr) - i - 1):
                if els[j].val > els[j + 1].val:
                    els[j], els[j + 1] = els[j + 1], els[j]
                    flag = True

                    # Play the swapping animation
                    self.play(*swap_elements(els[j], els[j + 1]))

                # Move window to next position
                if j != len(arr) - i - 2:
                    self.play(ApplyMethod(rectangle.shift, RIGHT * SCALE))

            # Move back to originate position
            self.play(ApplyMethod(rectangle.move_to, rect_pos))
            self.wait(0.1)
            # Mark last element as finished
            self.play(ApplyMethod(els[len(arr)-1-i].circle.set_color, BLUE_C))

            # If there is not any swapping happens, break the loop
            if not flag:
                break

        # Finished!
        self.play(FadeOut(rectangle))
        self.play(*[ApplyMethod(el.circle.set_color, BLUE_C) for el in els])

        self.wait(3)
