# This is a Python port of the kdbush https://github.com/mourner/kdbush
# which was released under the following license:
#
# ISC License
#
# Copyright (c) 2018, Vladimir Agafonkin
#
# Permission to use, copy, modify, and/or distribute this software for any purpose
# with or without fee is hereby granted, provided that the above copyright notice
# and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS
# OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
# TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF
# THIS SOFTWARE.
import numpy as np

from kdbush import KDBush

# fmt: off
POINTS = [
    [54,1],[97,21],[65,35],[33,54],[95,39],[54,3],[53,54],[84,72],[33,34],
    [43,15],[52,83],[81,23],[1,61],[38,74],[11,91],[24,56],[90,31],[25,57],
    [46,61],[29,69],[49,60],[4,98],[71,15],[60,25],[38,84],[52,38],[94,51],
    [13,25],[77,73],[88,87],[6,27],[58,22],[53,28],[27,91],[96,98],[93,14],
    [22,93],[45,94],[18,28],[35,15],[19,81],[20,81],[67,53],[43,3],[47,66],
    [48,34],[46,12],[32,38],[43,12],[39,94],[88,62],[66,14],[84,30],[72,81],
    [41,92],[26,4],[6,76],[47,21],[57,70],[71,82],[50,68],[96,18],[40,31],
    [78,53],[71,90],[32,14],[55,6],[32,88],[62,32],[21,67],[73,81],[44,64],
    [29,50],[70,5],[6,22],[68,3],[11,23],[20,42],[21,73],[63,86],[9,40],
    [99,2],[99,76],[56,77],[83,6],[21,72],[78,30],[75,53],[41,11],[95,20],
    [30,38],[96,82],[65,48],[33,18],[87,28],[10,10],[40,34],[10,20],[47,29],
    [46,78]
]

IDS = [
    97,74,95,30,77,38,76,27,80,55,72,90,88,48,43,46,65,39,62,93,9,96,47,8,3,12,
    15,14,21,41,36,40,69,56,85,78,17,71,44,19,18,13,99,24,67,33,37,49,54,57,98,
    45,23,31,66,68,0,32,5,51,75,73,84,35,81,22,61,89,1,11,86,52,94,16,2,6,25,92,
    42,20,60,58,83,79,64,10,59,53,26,87,4,63,50,7,28,82,70,29,34,91
]

COORDS = [
    10,20,6,22,10,10,6,27,20,42,18,28,11,23,13,25,9,40,26,4,29,50,30,38,41,11,
    43,12,43,3,46,12,32,14,35,15,40,31,33,18,43,15,40,34,32,38,33,34,33,54,1,61,
    24,56,11,91,4,98,20,81,22,93,19,81,21,67,6,76,21,72,21,73,25,57,44,64,47,66,
    29,69,46,61,38,74,46,78,38,84,32,88,27,91,45,94,39,94,41,92,47,21,47,29,48,
    34,60,25,58,22,55,6,62,32,54,1,53,28,54,3,66,14,68,3,70,5,83,6,93,14,99,2,
    71,15,96,18,95,20,97,21,81,23,78,30,84,30,87,28,90,31,65,35,53,54,52,38,65,
    48,67,53,49,60,50,68,57,70,56,77,63,86,71,90,52,83,71,82,72,81,94,51,75,53,
    95,39,78,53,88,62,84,72,77,73,99,76,73,81,88,87,96,98,96,82
]

NODE_SIZE = 10
# fmt: on


def test_index():
    index = KDBush(points=POINTS, node_size=NODE_SIZE)
    np.testing.assert_array_equal(index.ids, IDS)


def test_range_search():
    index = KDBush(points=POINTS, node_size=NODE_SIZE)
    result = index.range(20, 30, 50, 70)

    np.testing.assert_array_equal(
        result,
        [60, 20, 45, 3, 17, 71, 44, 19, 18, 15, 69, 90, 62, 96, 47, 8, 77, 72],
        err_msg="Result ids don't match",
    )

    for id in result:
        p = POINTS[id]
        assert (20 <= p[0] <= 50) and (30 <= p[1] <= 70), "result point not in range"

    for id in filter(lambda i: i not in result, IDS):
        p = POINTS[id]
        assert (p[0] < 20 or p[0] > 50) or (
            p[1] < 30 or p[1] > 70
        ), f"outside point {id}({p}) in range"


def test_radius_search():
    index = KDBush(points=POINTS, node_size=NODE_SIZE)

    qp = [50, 50]
    r = 20
    r2 = 20 * 20

    result = index.within(qp[0], qp[1], r)

    np.testing.assert_array_equal(
        result,
        [60, 6, 25, 92, 42, 20, 45, 3, 71, 44, 18, 96],
        err_msg="Result ids don't match",
    )

    for id in result:
        p = POINTS[id]
        assert sq_dist(*p, *qp) <= r2, f"result {id} outside radius"

    for id in filter(lambda i: i not in result, IDS):
        p = POINTS[id]
        assert sq_dist(*p, *qp) > r2, f"ouside point {id} inside radius"


def sq_dist(ax: float, ay: float, bx: float, by: float) -> float:
    return (ax - bx) ** 2 + (ay - by) ** 2
