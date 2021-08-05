#!/usr/bin/env python

import sys
from typing import List, Tuple
import math
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from numpy.core.numeric import convolve
from scipy import signal
from functools import reduce


def _plot(hz, gain, phase=None, title="no title", show=True, save=True, ext="png"):
    fig = plt.figure(figsize=(12, 5))

    ax1 = fig.add_subplot(111)
    ax1.set_title(title)
    ax1.set_ylabel("Gain (dB)")
    # -----
    # ax1.set_ylim(-18, 18)
    # ax1.set_yticks([-18, -15, -12, -9, -6, -3,
    #                 0, 3, 6, 9, 12, 15, 18])
    # ax1.set_yticklabels(["", "-15", "", "-9", "", "-3",
    #                     "0", "3", "", "9", "", "15", ""])
    # -----
    ax1.set_ylim(-12, 12)
    ax1.set_yticks([-12, -9, -6, -3, 0, 3, 6, 9, 12])
    # -----
    ax1.set_xlabel("Frequency (Hz)")
    ax1.set_xlim(20, 20000)
    ax1.set_xscale("log")
    ax1.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax1.set_xticks([20, 30, 40, 50, 60, 70, 80, 90, 100,
                    200, 300, 400, 500, 600, 700, 800, 900, 1000,
                    2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000,
                    20000])
    ax1.set_xticklabels(["20", "30", "40", "", "60", "", "80", "", "100",
                         "200", "", "400", "", "", "", "800", "", "1k",
                        "2k", "3k", "4k", "", "6k", "", "8k", "", "10k",
                         "20k"])
    ax1.grid()

    if phase is not None:
        ax2 = ax1.twinx()
        ax2.set_ylabel("Phase (deg.)")
        ax2.set_ylim(-180, 180)
        # -----
        # ax2.set_yticks([-180, -150, -120, -90, -60, -30,
        #                 0, 30, 60, 90, 120, 150, 180])
        # ax2.set_yticklabels(["-180", "", "-120", "", "-60", "",
        #                      "0", "", "60", "", "120", "", "180"])
        # -----
        ax2.set_yticks([-180, -135, -90, -45, 0, 45, 90, 135, 180])
        # -----

    # plot
    if phase is not None:
        ax2.plot(hz, phase, "cyan")
    ax1.plot(hz, gain, "blue")

    if save:
        plt.savefig(title+"."+ext)

    if show:
        plt.show()


def plot_from_coeff(b, a, n, title="no title", fs=48000.0, show=True, save=True, ext="png"):
    w, h = signal.freqz(b, a, worN=n)
    mag = np.abs(h)
    gain = 20*np.log10(mag/1.0)
    phase = np.angle(h)
    phase_deg = phase*180/math.pi
    hz = fs/2 * w/math.pi  # [0..fs/2]
    _plot(hz, gain, phase_deg, title, show, save, ext)


def plot_from_ir(ir, n, title="no title", fs=48000.0, show=True, save=True, ext="png"):
    h = np.fft.fft(ir, n)
    mag = np.abs(h)
    gain = 20*np.log10(mag/1.0)
    phase = np.angle(h)
    phase_deg = phase*180/math.pi
    hz = np.linspace(0, fs, n, endpoint=False)  # [0..fs]
    _plot(hz, gain, phase_deg, title, show, save, ext)


def load_dataset1():
    t = "HPF 250Hz Q=0.707"
    b0, b1, b2 = 0.9997322937381828, -1.9994645874763657, 0.9997322937381828
    a0, a1, a2 = 1.0231393796476493, -1.9989291749527314, 0.9768606203523507
    b, a = [b0, b1, b2], [a0, a1, a2]
    ir = [0.9771223, -0.045219973, -0.044149913, -0.043082047, -0.042017393, -0.04095692, -0.039901547, -0.03885215, -0.03780956, -0.036774553, -0.035747875, -0.034730222, -0.033722248, -0.032724574, -0.03173778, -0.0307624, -0.029798945, -0.02884788, -0.027909642, -0.02698463, -0.02607322, -0.025175743, -0.024292512, -0.023423808, -0.022569882, -0.021730958, -0.020907236, -0.020098893, -0.019306075, -0.018528914, -0.017767511, -0.017021954, -0.016292306, -0.015578608, -0.014880887, -0.014199153, -0.013533392, -0.012883582, -0.01224968, -0.011631629, -0.011029362, -0.010442792, -0.009871825, -0.009316352, -0.008776253, -0.0082514, -0.0077416496, -0.0072468547, -0.0067668557, -0.006301486, -0.0058505703, -0.0054139276, -0.0049913684, -0.004582699, -0.004187718, -0.0038062201, -0.0034379945, -0.0030828263, -0.0027404965, -0.002410783, -0.00209346, -0.0017882988, -0.0014950694, -0.0012135385, -0.0009434717, -0.00068463315, -0.0004367859, -0.00019969216, 0.000026886315, 0.00024318803, 0.00044945144, 0.0006459147, 0.00083281554, 0.0010103908, 0.0011788765, 0.0013385074, 0.0014895169, 0.001632137, 0.001766598, 0.001893128, 0.0020119534, 0.0021232984, 0.0022273848, 0.002324432, 0.0024146566, 0.002498273, 0.0025754927, 0.002646524, 0.0027115725, 0.0027708407, 0.0028245281, 0.002872831, 0.0029159423, 0.0029540518, 0.0029873457, 0.0030160071, 0.0030402157, 0.0030601472, 0.0030759743, 0.0030878664, 0.0030959886, 0.0031005032, 0.0031015687, 0.0030993398, 0.003093968, 0.0030856007, 0.0030743827, 0.0030604545, 0.003043953, 0.0030250123, 0.003003762, 0.0029803296, 0.0029548376, 0.002927406, 0.0028981515, 0.0028671871, 0.0028346223, 0.0028005638, 0.0027651147, 0.0027283751, 0.002690442, 0.0026514085, 0.0026113656, 0.002570401, 0.002528599, 0.0024860415, 0.002442807, 0.0023989715, 0.0023546077, 0.0023097864, 0.002264575, 0.0022190385, 0.0021732394, 0.0021272372, 0.0020810894, 0.002034851, 0.0019885744, 0.0019423096, 0.0018961045, 0.001850005, 0.0018040545, 0.0017582943, 0.0017127637, 0.0016674999, 0.0016225382, 0.0015779121, 0.0015336531, 0.0014897909, 0.0014463535, 0.001403367, 0.0013608561, 0.0013188439, 0.0012773516, 0.0012363992, 0.0011960051, 0.0011561865, 0.0011169588, 0.0010783364, 0.0010403325, 0.0010029586, 0.0009662257, 0.00093014294, 0.0008947188, 0.00085996056, 0.00082587445, 0.00079246575, 0.0007597388, 0.00072769704, 0.00069634296, 0.0006656783, 0.00063570397, 0.0006064201, 0.0005778261, 0.0005499208, 0.00052270206, 0.00049616746, 0.00047031377, 0.0004451373, 0.00042063367, 0.0003967982, 0.00037362555, 0.00035111, 0.00032924543, 0.00030802522, 0.0002874425, 0.0002674899, 0.00024815986, 0.00022944444, 0.00021133541, 0.00019382431, 0.00017690241, 0.00016056078, 0.00014479028, 0.00012958156, 0.00011492515, 0.0001008114, 0.000087230525, 0.000074172654, 0.00006162778, 0.000049585848, 0.0000380367, 0.00002697013, 0.0000163759, 0.000006243728, -0.0000034366776, -0.000012675621, -0.000021483402, -0.000029870303, -0.000037846585, -0.000045422472, -0.000052608146, -0.000059413735, -0.000065849315, -0.00007192488, -0.00007765035, -0.000083035586, -0.000088090324, -0.00009282423, -0.00009724686, -0.00010136767, -0.00010519599, -0.00010874106, -0.000112011956, -0.000115017676, -0.00011776706, -0.00012026883, -0.00012253156, -0.00012456371, -0.00012637356, -0.0001279693, -0.00012935892, -0.00013055028, -0.00013155113, -0.00013236904, -0.0001330114, -0.00013348549, -0.00013379844, -0.0001339572, -0.00013396857, -0.00013383922, -0.00013357564, -0.00013318419, -0.00013267105, -0.00013204226, -0.00013130372, -0.00013046117, -0.00012952018, -0.0001284862, -0.0001273645, -0.00012616024, -0.00012487842, -0.00012352389, -0.00012210134, -0.00012061533, -0.00011907031, -0.000117470554, -0.00011582021, -0.00011412329, -
          0.0001123837, -0.00011060516, -0.00010879131, -0.00010694565, -0.00010507153, -0.00010317222, -0.00010125084, -0.0000993104, -0.00009735378, -0.00009538378, -0.000093403054, -0.000091414164, -0.00008941956, -0.0000874216, -0.00008542251, -0.000083424435, -0.000081429425, -0.00007943943, -0.0000774563, -0.00007548182, -0.000073517636, -0.00007156536, -0.00006962648, -0.000067702436, -0.00006579456, -0.00006390412, -0.000062032304, -0.000060180235, -0.00005834895, -0.000056539433, -0.000054752585, -0.00005298926, -0.000051250234, -0.00004953623, -0.000047847905, -0.000046185873, -0.000044550678, -0.00004294282, -0.000041362742, -0.000039810846, -0.00003828748, -0.000036792942, -0.000035327503, -0.00003389137, -0.00003248473, -0.000031107716, -0.000029760427, -0.000028442933, -0.000027155264, -0.000025897418, -0.000024669362, -0.000023471033, -0.000022302343, -0.000021163176, -0.000020053383, -0.000018972802, -0.00001792124, -0.000016898488, -0.000015904308, -0.000014938453, -0.000014000651, -0.000013090615, -0.00001220804, -0.000011352609, -0.00001052399, -0.000009721836, -0.000008945791, -0.000008195485, -0.000007470539, -0.000006770565, -0.000006095167, -0.000005443939, -0.0000048164698, -0.000004212341, -0.0000036311303, -0.0000030724082, -0.0000025357429, -0.0000020206978, -0.0000015268347, -0.000001053712, -0.0000006008869, -0.00000016791506, 0.00000024564827, 0.0000006402482, 0.0000010163294, 0.000001374336, 0.0000017147107, 0.000002037895, 0.000002344328, 0.000002634447, 0.000002908686, 0.0000031674763, 0.0000034112459, 0.000003640419, 0.000003855416, 0.0000040566533, 0.000004244542, 0.0000044194903, 0.0000045818997, 0.0000047321673, 0.0000048706856, 0.0000049978403, 0.000005114013, 0.0000052195787, 0.0000053149065, 0.00000540036, 0.000005476296, 0.0000055430655, 0.0000056010135, 0.0000056504787, 0.0000056917925, 0.0000057252805, 0.0000057512616, 0.000005770048, 0.000005781946, 0.0000057872544, 0.000005786266, 0.000005779266, 0.000005766534, 0.000005748342, 0.0000057249576, 0.0000056966387, 0.0000056636386, 0.0000056262033, 0.0000055845735, 0.0000055389814, 0.0000054896545, 0.000005436813, 0.0000053806716, 0.0000053214385, 0.0000052593145, 0.0000051944967, 0.0000051271736, 0.00000505753, 0.000004985743, 0.000004911985, 0.0000048364222, 0.0000047592157, 0.0000046805203, 0.0000046004857, 0.0000045192564, 0.0000044369717, 0.000004353765, 0.0000042697648, 0.000004185096, 0.000004099876, 0.00000401422, 0.000003928237, 0.0000038420326, 0.0000037557056, 0.0000036693527, 0.0000035830656, 0.0000034969312, 0.000003411033, 0.00000332545, 0.000003240258, 0.0000031555278, 0.0000030713277, 0.0000029877215, 0.00000290477, 0.0000028225306, 0.000002741057, 0.0000026603998, 0.0000025806064, 0.0000025017214, 0.0000024237863, 0.0000023468394, 0.0000022709169, 0.0000021960518, 0.0000021222745, 0.0000020496132, 0.0000019780935, 0.0000019077381, 0.0000018385688, 0.0000017706037, 0.0000017038597, 0.0000016383514, 0.0000015740915, 0.0000015110908, 0.0000014493581, 0.0000013889008, 0.0000013297247, 0.0000012718333, 0.0000012152295, 0.0000011599141, 0.0000011058868, 0.0000010531458, 0.0000010016881, 0.0000009515096, 0.00000090260494, 0.00000085496765, 0.0000008085903, 0.0000007634644, 0.00000071958067, 0.00000067692866, 0.0000006354975, 0.0000005952752, 0.00000055624923, 0.0000005184063, 0.00000048173257, 0.00000044621342, 0.0000004118339, 0.0000003785784, 0.00000034643088, 0.0000003153749, 0.00000028539358, 0.0000002564697, 0.00000022858565, 0.00000020172362, 0.0000001758655, 0.00000015099293, 0.00000012708738, 0.00000010413011, 0.00000008210226, 0.00000006098485, 0.000000040758803, 0.000000021404958, 0.0000000029041285, -0.000000014762909, -0.00000003161538, -0.000000047672486, -0.000000062953404]
    return t, b, a, ir


def load_dataset2():
    t = "HPF 250Hz Q=0.707 & LPF 8kHz Q=0.707"
    vb, va = [None, None], [None, None]
    b0, b1, b2 = 0.9997322937381828, -1.9994645874763657, 0.9997322937381828
    a0, a1, a2 = 1.0231393796476493, -1.9989291749527314, 0.9768606203523507
    vb[0], va[0] = [b0, b1, b2], [a0, a1, a2]
    b0, b1, b2 = 0.24999999999999994, 0.4999999999999999, 0.24999999999999994
    a0, a1, a2 = 1.6124649248829126, -1.0000000000000002, 0.3875350751170873
    vb[1], va[1] = [b0, b1, b2], [a0, a1, a2]
    b = signal.convolve(vb[0], vb[1])
    a = signal.convolve(va[0], va[1])
    ir = [0.15149513, 0.38993177, 0.33604154, 0.08730661, -0.053337052, -0.08011949, -0.0622697, -0.044108637, -0.03648501, -0.03547539, -0.036039732, -0.035995763, -0.035201848, -0.034095038, -0.032980796, -0.031943895, -0.03096381, -0.030007768, -0.029060658, -0.028121259, -0.027192693, -0.026277423, -0.02537643, -0.024489928, -0.023617987, -0.02276075, -0.021918437, -0.021091267, -0.020279435, -0.019483102, -0.018702399, -0.017937437, -0.017188301, -0.01645506, -0.015737765, -0.015036442, -0.014351104, -0.013681746, -0.013028344, -0.012390862, -0.011769246, -0.01116343, -0.010573332, -0.009998859, -0.009439906, -0.008896356, -0.0083680805, -0.007854942, -0.0073567936, -0.0068734773, -0.0064048283, -0.0059506744, -0.0055108345, -0.0050851214, -0.0046733427, -0.004275298, -0.0038907838, -0.0035195895, -0.0031615014, -0.0028163018, -0.0024837684, -0.002163677, -0.0018557993, -0.0015599054, -0.0012757626, -0.0010031371, -0.0007417931, -0.0004914938, -0.00025200174, -0.000023078655, 0.0001955139, 0.00040401443, 0.00060266117, 0.000791692, 0.00097134395, 0.0011418533, 0.001303455, 0.0014563829, 0.0016008693, 0.0017371448, 0.0018654382, 0.0019859762, 0.0020989834, 0.0022046824, 0.002303293, 0.0023950324, 0.0024801155, 0.0025587548, 0.0026311588, 0.002697534, 0.0027580836, 0.002813008, 0.0028625038, 0.0029067649, 0.0029459817, 0.0029803414, 0.0030100276, 0.003035221, 0.003056098, 0.003072832, 0.0030855932, 0.0030945477, 0.0030998585, 0.0031016846, 0.0031001822, 0.0030955027, 0.003087795, 0.0030772046, 0.0030638725, 0.0030479366, 0.0030295318, 0.0030087885, 0.0029858344, 0.0029607937, 0.002933787, 0.002904931, 0.0028743402, 0.0028421248, 0.0028083918, 0.0027732453, 0.0027367861, 0.0026991118, 0.0026603166, 0.002620492, 0.0025797258, 0.0025381038, 0.0024957082, 0.002452618, 0.00240891, 0.0023646578, 0.0023199324, 0.002274802, 0.002229332, 0.0021835854, 0.0021376228, 0.002091502, 0.0020452784, 0.001999005, 0.0019527322, 0.0019065088, 0.0018603809, 0.0018143923, 0.001768585, 0.0017229985, 0.0016776707, 0.0016326373, 0.0015879322, 0.0015435872, 0.0014996326, 0.0014560965, 0.0014130058, 0.0013703852, 0.0013282582, 0.0012866466, 0.0012455705, 0.0012050488, 0.0011650986, 0.0011257362, 0.0010869759, 0.0010488313, 0.0010113143, 0.0009744358, 0.00093820563, 0.00090263225, 0.0008677232, 0.00083348504, 0.00079992315, 0.00076704216, 0.00073484564, 0.0007033364, 0.0006725162, 0.0006423862, 0.0006129468, 0.0005841974, 0.00055613706, 0.00052876386, 0.00050207536, 0.00047606858, 0.0004507399, 0.00042608514, 0.0004020996, 0.00037877815, 0.00035611517, 0.00033410455, 0.00031273984, 0.00029201419, 0.00027192038, 0.00025245085, 0.00023359778, 0.00021535296, 0.00019770802, 0.00018065427, 0.00016418281, 0.00014828458, 0.00013295024, 0.00011817038, 0.00010393535, 0.00009023543, 0.00007706074, 0.00006440131, 0.000052247102, 0.00004058797, 0.000029413724, 0.000018714129, 0.000008478913, -0.0000013022183, -0.000010639565, -0.000019543428, -0.000028024097, -0.000036091835, -0.00004375688, -0.000051029423, -0.000057919602, -0.00006443751, -0.00007059315, -0.000076396485, -0.00008185736, -0.00008698556, -0.00009179075, -0.00009628253, -0.000100470366, -0.00010436362, -0.00010797156, -0.00011130329, -0.00011436783, -0.00011717406, -0.000119730714, -0.000122046426, -0.00012412966, -0.00012598874, -0.00012763187, -0.00012906709, -0.00013030232, -0.0001313453, -0.00013220364, -0.00013288479, -0.00013339605, -0.00013374457, -0.00013393736, -0.00013398123, -0.00013388289, -0.00013364888, -0.00013328559, -0.00013279922, -0.00013219587, -0.00013148146, -0.00013066173, -0.00012974236, -0.00012872876, -0.00012762629, -0.0001264401, -0.00012517524, -0.00012383658, -0.00012242887, -0.0001209567, -0.00011942451, -0.000117836644, -
          0.00011619727, -0.00011451043, -0.00011278005, -0.000111009904, -0.00010920363, -0.00010736478, -0.00010549673, -0.00010360275, -0.000101686026, -0.000099749566, -0.0000977963, -0.000095829026, -0.00009385044, -0.00009186313, -0.00008986956, -0.000087872104, -0.00008587304, -0.00008387452, -0.00008187861, -0.00007988728, -0.00007790241, -0.0000759258, -0.00007395912, -0.000072004, -0.00007006195, -0.00006813441, -0.000066222754, -0.000064328255, -0.00006245212, -0.00006059549, -0.00005875941, -0.00005694489, -0.00005515284, -0.000053384127, -0.000051639545, -0.00004991983, -0.00004822565, -0.00004655763, -0.000044916334, -0.000043302265, -0.00004171588, -0.000040157596, -0.000038627764, -0.0000371267, -0.000035654677, -0.00003421192, -0.000032798616, -0.000031414915, -0.000030060917, -0.000028736704, -0.000027442311, -0.000026177744, -0.00002494298, -0.00002373796, -0.000022562603, -0.000021416794, -0.000020300398, -0.000019213252, -0.000018155173, -0.00001712595, -0.000016125357, -0.000015153147, -0.000014209052, -0.000013292789, -0.000012404058, -0.000011542545, -0.000010707919, -0.000009899838, -0.000009117946, -0.00000836188, -0.000007631259, -0.000006925699, -0.0000062448044, -0.0000055881724, -0.0000049553923, -0.000004346048, -0.0000037597174, -0.0000031959726, -0.0000026543821, -0.0000021345109, -0.0000016359206, -0.0000011581704, -0.00000070081774, -0.0000002634186, 0.00000015447173, 0.0000005532984, 0.0000009335061, 0.0000012955393, 0.0000016398409, 0.0000019668528, 0.0000022770148, 0.0000025707643, 0.0000028485363, 0.000003110763, 0.0000033578726, 0.0000035902908, 0.0000038084384, 0.000004012733, 0.0000042035867, 0.000004381409, 0.0000045466018, 0.0000046995638, 0.000004840689, 0.000004970364, 0.000005088972, 0.0000051968887, 0.000005294485, 0.000005382126, 0.000005460169, 0.000005528968, 0.000005588868, 0.0000056402096, 0.0000056833255, 0.000005718543, 0.000005746183, 0.000005766558, 0.0000057799766, 0.0000057867387, 0.0000057871384, 0.0000057814636, 0.000005769994, 0.0000057530046, 0.0000057307625, 0.0000057035286, 0.000005671557, 0.000005635096, 0.000005594386, 0.000005549663, 0.0000055011537, 0.0000054490815, 0.0000053936615, 0.000005335103, 0.00000527361, 0.0000052093787, 0.000005142601, 0.000005073461, 0.0000050021386, 0.000004928807, 0.0000048536335, 0.0000047767808, 0.000004698405, 0.0000046186565, 0.0000045376814, 0.0000044556205, 0.0000043726072, 0.0000042887727, 0.0000042042416, 0.000004119134, 0.0000040335644, 0.000003947644, 0.000003861478, 0.0000037751686, 0.0000036888116, 0.0000036025, 0.0000035163223, 0.0000034303623, 0.0000033447002, 0.0000032594123, 0.0000031745708, 0.000003090244, 0.0000030064975, 0.0000029233925, 0.0000028409866, 0.0000027593348, 0.0000026784885, 0.0000025984955, 0.0000025194013, 0.0000024412477, 0.0000023640744, 0.0000022879174, 0.0000022128106, 0.000002138785, 0.0000020658695, 0.0000019940896, 0.0000019234697, 0.000001854031, 0.0000017857926, 0.0000017187717, 0.0000016529835, 0.000001588441, 0.0000015251555, 0.0000014631362, 0.0000014023909, 0.0000013429254, 0.0000012847443, 0.00000122785, 0.0000011722442, 0.0000011179267, 0.0000010648961, 0.0000010131496, 0.0000009626833, 0.00000091349216, 0.00000086557, 0.00000081890954, 0.00000077350256, 0.0000007293399, 0.00000068641145, 0.00000064470635, 0.0000006042129, 0.0000005649187, 0.0000005268106, 0.0000004898748, 0.00000045409706, 0.0000004194623, 0.00000038595516, 0.00000035355967, 0.00000032225947, 0.00000029203775, 0.0000002628774, 0.00000023476086, 0.00000020767041, 0.00000018158796, 0.00000015649523, 0.00000013237371, 0.00000010920473, 0.00000008696942, 0.00000006564884, 0.000000045223924, 0.00000002567554, 0.000000006984499, -0.000000010868416, -0.000000027902432, -0.000000044136762]
    return t, b, a, ir


# returns (result_type, [b], [a], ir)
#
# result_type
#   0: error
#   1: coefficients
#   2: impulse response
#
# [b]
#   [[b0, b1, b2, ...], ...]
#
# [a]
#   [[a0, a1, a2, ...], ...]
#
# ir
#   [t0, t1, t2, ...]
def parse_input(file: str) -> Tuple[int, List[list], List[list], list]:
    buf = []
    if file == "":
        buf = sys.stdin.read().splitlines()
    else:
        with open(file) as f:
            buf = f.read().splitlines()
    if len(buf) == 0:
        return 0, [[]], [[]], []

    result_type = 1
    vb, va = [], []
    ir = []
    if buf[0] not in ["b", "a"]:
        result_type = 2

    # Coeff.
    if result_type == 1:
        tmp = []
        is_a = False
        for x in buf:
            if x in ["b", "a"]:
                if len(tmp) != 0:
                    if is_a:
                        va.append(tmp)
                    else:
                        vb.append(tmp)
                    tmp = []
                if x == "a":
                    is_a = True
                else:
                    is_a = False
                continue
            try:
                tmp.append(float(x))
            except Exception as e:
                print(f"{e}", file=sys.stderr)
                return 0, [[]], [[]], []
        if is_a:
            va.append(tmp)
        else:
            vb.append(tmp)

    # IR
    if result_type == 2:
        try:
            ir = [float(x) for x in buf]
        except Exception as e:
            print(f"{e}", file=sys.stderr)
            return 0, [[]], [[]], []

    return result_type, vb, va, ir


# requires len(v) != 0
def convolve_coeffs(v: List[list]) -> list:
    return reduce(lambda x, y: signal.convolve(x, y), v, [1.0])


def main():
    # # demo
    # t, b, a, ir = load_dataset1()
    # t, b, a, ir = load_dataset2()
    # plot_from_coeff(b, a, n=2400, title=t+" (Coeff.)", show=True, save=False)
    # plot_from_ir(ir, n=2400, title=t+" (IR)", show=True, save=False)
    # exit(0)

    import argparse
    from argparse import RawTextHelpFormatter
    from datetime import datetime as dt
    import textwrap
    help = textwrap.dedent("""\
        Plot frequency response and phase from coefficients or impulse response.

        Coefficients format:
        ----------
        b
        1.234
        ...
        a
        -1.234
        ...
        b
        1.111
        ...
        a
        1.111
        ...
        ----------

        Impulse response format:
        ----------
        1.111
        1.234
        -1.111
        ...
        ----------
        """)
    parser = argparse.ArgumentParser(
        description=help, formatter_class=RawTextHelpFormatter)
    parser.add_argument("-i", dest="file", type=str, nargs=1,
                        default="", help="input file (default: use stdin)")
    parser.add_argument("-t", dest="title",  type=str, nargs=1,
                        default="", help="title (default: {yyyyMMddHHmmss}-{Coeff|IR})")
    parser.add_argument("-r", dest="rate", type=float, nargs=1,
                        default=48000.0, help="sampling rate (default: 48000)")
    parser.add_argument("-n", dest="show",
                        action="store_false", help="no show plot")
    parser.add_argument("-s", dest="save",
                        action="store_true", help="save PNG")
    # parser.add_argument("--dump", dest="dump", action="store_true", help="dump PNG to stdout")

    args = parser.parse_args()
    # print(args, file=sys.stderr)

    is_coeff = False
    file = ""
    if len(args.file) != 0:
        file = args.file[0]
    result_type, vb, va, ir = parse_input(file)
    if result_type == 0:
        print("wrong format", file=sys.stderr)
        exit(1)
    if result_type == 1:
        is_coeff = True
    title = args.title
    if title == "":
        title = dt.now().strftime("%Y%m%d%H%M%S")
        if is_coeff:
            title += " (Coeff.)"
        else:
            title += " (IR)"

    if is_coeff:
        b = convolve_coeffs(vb)
        a = convolve_coeffs(va)
        plot_from_coeff(b, a, n=2400, title=title, fs=args.rate,
                        show=args.show, save=args.save)
    else:
        plot_from_ir(ir, n=2400, title=title, fs=args.rate,
                     show=args.show, save=args.save)

    exit(0)


if __name__ == "__main__":
    main()
