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
    return [
        *swap_mobjects(e1.text, e2.text),
        *swap_mobjects(e1.circle, e2.circle),
    ]


def move_el(el, direction):
    """Move 1 unit to a specific direction.
    :param el: Element
    :param direction: ndarray
    """
    return [
        ApplyMethod(el.circle.shift, direction * SCALE),
        ApplyMethod(el.text.shift, direction * SCALE)
    ]


class SelectionSort(Scene):
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

        # Selection sort
        for i in range(len(arr)):
            min_idx = i
            min_el = els[i]
            for j in range(i, len(arr)):
                if els[j].val < min_el.val:
                    min_el = els[j]
                    min_idx = j

            # If arr[i] is the min value, don't play animation
            if i != min_idx:
                self.play(*move_el(els[i], UP), *move_el(els[min_idx], DOWN))
                self.play(*swap_elements(els[i], els[min_idx]))
                self.play(*move_el(els[i], UP), *move_el(els[min_idx], DOWN))
            els[i], els[min_idx] = els[min_idx], els[i]

            # Mark ith element as finished
            self.play(ApplyMethod(els[i].circle.set_color, BLUE_C))
        self.wait(3)
