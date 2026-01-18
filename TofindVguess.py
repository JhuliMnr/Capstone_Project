import math
import numpy as np
import matplotlib.pyplot as plt
grid = []
for y in range(7405000,7427000, 120):
    for x in range(620000, 640000, 120):
        grid.append([x,y])

BB1 = [630006.7,7413884.8]
BB2 = [627994.1,7417545.5]
BB3 = [626036.7,7414616.9]
BB4 = [626724.1,7416094.8]
BB5 = [632215.5,7413976]

dBB1 = []
dBB2 = []
dBB3 = []
dBB4 = []
dBB5 = []
for i in range(0,len(grid)):
    distance1 = math.sqrt(pow(BB1[0] - grid[i][0], 2) + pow(BB1[1] - grid[i][1], 2))
    dBB1.append(distance1)
    distance2 = math.sqrt(pow(BB2[0] - grid[i][0], 2) + pow(BB2[1] - grid[i][1], 2))
    dBB2.append(distance2)
    distance3 = math.sqrt(pow(BB3[0] - grid[i][0], 2) + pow(BB3[1] - grid[i][1], 2))
    dBB3.append(distance3)
    distance4 = math.sqrt(pow(BB4[0] - grid[i][0], 2) + pow(BB4[1] - grid[i][1], 2))
    dBB4.append(distance4)
    distance5 = math.sqrt(pow(BB5[0] - grid[i][0], 2) + pow(BB5[1] - grid[i][1], 2))
    dBB5.append(distance5)
#================================================
#============== for one event ==============
#==================================================================
# ebb1 = 58972.57
# ebb3 = 58971.09
# ebb4 = 58971.19
# ebb5 = 58972.68
# ebb1 = 15708.29
# ebb3 = 15708.8
# ebb4 = 15708.82
# ebb5 = 15708.76
# ebb1 = 22432.31
# ebb3 = 22432.05
# ebb4 = 22432.65
# ebb5 = 22432.2
#=====================================================
# Class1 = [[58972.57,58971.09,58971.19,58972.68],[15708.29,15708.8,15708.82,15708.76],
#           [22432.31,22432.05,22432.65,22432.2],[22852.49,22851.85,22851.92,22852.97]]
# 25176.16	 BB1
# 25175.31	 BB3
# 25175.14	 BB4
# 25176.52	 BB5
# 68889.25	 BB1
# 68887.76	 BB3
# 68887.83	 BB4
# 68888.84	 BB5


# class1 = [[68031.76,68031.17,68031.14,68031.65],
#           [68889.25,68887.76,68887.83,68888.84], #4.2
#           [69016.44,69016.73,69016.61,69016.8], #4.8
#           [69842.11,69842.02,69842.12,69841.78],
#           [70952.46,70952.12,70952.39,70952.13],
#           [71249.36,71248.92,71249.05,71249.07]]
class1 = [[25176.16,25175.31,25175.14,25176.52],[68889.25,68887.76,68887.83,68888.84]]
misfit_all= []
vguess = np.arange(3000, 5700, 300)
for sublist in class1:
    thbb1 = []
    thbb3 = []
    thbb4 = []
    thbb5 = []
    for vg in vguess:
        for elem1 in dBB1:
            temp1 = elem1/vg
            temp21 = sublist[0] - temp1
            thbb1.append(temp21)
        for elem3 in dBB3:
            temp3 = elem3/vg
            temp23 = sublist[1] - temp3
            thbb3.append(temp23)
        for elem4 in dBB4:
            temp4 = elem4/vg
            temp24 = sublist[2] - temp4
            thbb4.append(temp24)
        for elem5 in dBB5:
            temp5 = elem5/vg
            temp25 = sublist[3] - temp5
            thbb5.append(temp25)
    th1 = np.split(np.array(thbb1),len(vguess))
    th3 = np.split(np.array(thbb3),len(vguess))
    th4 = np.split(np.array(thbb4),len(vguess))
    th5 = np.split(np.array(thbb5),len(vguess))
    import statistics as stat
    vguesstdev = []
    for e in range(0,len(th1)):
        for i in range(0,len(th1[e])):
            vguesstdev.append(stat.stdev([th1[e][i],th3[e][i],th4[e][i],th5[e][i]]))
    vguesstdev = np.array(vguesstdev)
    vgstdev = np.split(vguesstdev,len(vguess))
    stgrid = []
    for j in range(0,len(vgstdev[0])):
        mins = []
        for k in range(0,len(vgstdev)):
            mins.append(vgstdev[k][j])
        stgrid.append(min(mins))
    index = []
    for g in range(0,len(stgrid)):
        u = np.where(vgstdev == stgrid[g])[0][0]
        index.append(u)
    misfit = list()
    x = np.arange(620000, 640000, 120)
    y = np.arange(7405000,7427000, 120)
    X, Y = np.meshgrid(x, y)
    for sublist in vgstdev:
        z = np.array(sublist)
        misfit.append(min(z))
    print(min(misfit), vguess[np.argmin(misfit)])
    misfit_all.append(misfit)
    plt.plot(vguess,misfit)
    plt.show()
# vguess = np.arange(3300, 5700, 300)
# thbb1 = []
# thbb3 = []
# thbb4 = []
# thbb5 = []
# for vg in vguess:
#     for elem1 in dBB1:
#         temp1 = elem1/vg
#         temp21 = ebb1 - temp1
#         thbb1.append(temp21)
#     for elem3 in dBB3:
#         temp3 = elem3/vg
#         temp23 = ebb3 - temp3
#         thbb3.append(temp23)
#     for elem4 in dBB4:
#         temp4 = elem4/vg
#         temp24 = ebb4 - temp4
#         thbb4.append(temp24)
#     for elem5 in dBB5:
#         temp5 = elem5/vg
#         temp25 = ebb5 - temp5
#         thbb5.append(temp25)
# th1 = np.split(np.array(thbb1),len(vguess))
# th3 = np.split(np.array(thbb3),len(vguess))
# th4 = np.split(np.array(thbb4),len(vguess))
# th5 = np.split(np.array(thbb5),len(vguess))
# import statistics as stat
# vguesstdev = []
# for e in range(0,len(th1)):
#     for i in range(0,len(th1[e])):
#         vguesstdev.append(stat.stdev([th1[e][i],th3[e][i],th4[e][i],th5[e][i]]))
# vguesstdev = np.array(vguesstdev)
# vgstdev = np.split(vguesstdev,len(vguess))
# stgrid = []
# for j in range(0,len(vgstdev[0])):
#     mins = []
#     for k in range(0,len(vgstdev)):
#         mins.append(vgstdev[k][j])
#     stgrid.append(min(mins))
# index = []
# for g in range(0,len(stgrid)):
#     u = np.where(vgstdev == stgrid[g])[0][0]
#     index.append(u)
# misfit = list()
# x = np.arange(620000, 640000, 120)
# y = np.arange(7405000,7427000, 120)
# X, Y = np.meshgrid(x, y)
# for sublist in vgstdev:
#     z = np.array(sublist)
#     misfit.append(min(z))
# print(min(misfit), vguess[np.argmin(misfit)])
# plt.plot(vguess,misfit)
# plt.show()
#
# plt.plot(np.log10(vguess),np.log10(misfit))
# plt.show()
#===========================================
#============================================
#2303.25	 'BB3'	2303.42	 'BB4'	2303.7	 'BB2'	2304.62	 'BB5'
#2807.64	 'BB3'	2807.79	 'BB4'	2807.9	 'BB2'	2808.99	 'BB5'
#2955.5	 'BB2'	2955.71	 'BB4'	2955.74	 'BB5'	2955.94	 'BB3'
#3321.01	 'BB5'	3321.25	 'BB3'	3321.64	 'BB2'	3322.35	 'BB4'
#9555.1	 'BB3'	9555.13	 'BB4'	9555.41	 'BB2'	9556.42	 'BB5'

#=======================================================
# class2 = [[2303.7,2303.25,2303.42,2304.62],[2807.9,2807.64,2807.79,2808.99],
#           [2955.5,2955.94,2955.71,2955.74],[3321.64,3321.25,3322.35,3321.01],
#           [9555.41,9555.1,9555.13,9556.42]]
# misfit_all= []
# vguess = np.arange(3000, 5700, 300)
# for sublist in class2:
#     thbb2 = []
#     thbb3 = []
#     thbb4 = []
#     thbb5 = []
#     for vg in vguess:
#         for elem2 in dBB2:
#             temp2 = elem2/vg
#             temp22 = sublist[0] - temp2
#             thbb2.append(temp22)
#         for elem3 in dBB3:
#             temp3 = elem3/vg
#             temp23 = sublist[1] - temp3
#             thbb3.append(temp23)
#         for elem4 in dBB4:
#             temp4 = elem4/vg
#             temp24 = sublist[2] - temp4
#             thbb4.append(temp24)
#         for elem5 in dBB5:
#             temp5 = elem5/vg
#             temp25 = sublist[3] - temp5
#             thbb5.append(temp25)
#     th2 = np.split(np.array(thbb2),len(vguess))
#     th3 = np.split(np.array(thbb3),len(vguess))
#     th4 = np.split(np.array(thbb4),len(vguess))
#     th5 = np.split(np.array(thbb5),len(vguess))
#     import statistics as stat
#     vguesstdev = []
#     for e in range(0,len(th2)):
#         for i in range(0,len(th2[e])):
#             vguesstdev.append(stat.stdev([th2[e][i],th3[e][i],th4[e][i],th5[e][i]]))
#     vguesstdev = np.array(vguesstdev)
#     vgstdev = np.split(vguesstdev,len(vguess))
#     stgrid = []
#     for j in range(0,len(vgstdev[0])):
#         mins = []
#         for k in range(0,len(vgstdev)):
#             mins.append(vgstdev[k][j])
#         stgrid.append(min(mins))
#     index = []
#     for g in range(0,len(stgrid)):
#         u = np.where(vgstdev == stgrid[g])[0][0]
#         index.append(u)
#     misfit = list()
#     x = np.arange(620000, 640000, 120)
#     y = np.arange(7405000,7427000, 120)
#     X, Y = np.meshgrid(x, y)
#     for sublist in vgstdev:
#         z = np.array(sublist)
#         misfit.append(min(z))
#     print(min(misfit), vguess[np.argmin(misfit)])
#     misfit_all.append(misfit)

