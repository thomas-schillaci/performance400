import numpy as np
import math as m
import scipy.signal
import matplotlib.pyplot as pl
import time

#
def get_speed_profiles(trajectory, refresh_rate, windows_size_for_average=6, savgol1=13, savgol2=7, medfilt=11):
    """

    Calculate speed profiles

    :param trajectory: the trajectory as generated by trajectory_utils.py
    :param refresh_rate: the refresh rate associate withe the trajectory
    :param windows_size_for_average:  number of points taken for the sliding windows average
    :param savgol1: first parameter for scipy.savgol filter
    :param savgol2: second parameter for scipy.savgol filter
    :param medfilt: size of the median filter, must be odd
    :return: the raw speed profile,the filtered speed profile, the median speed profile, the mean speed profile
            and the index needed to interpret all this profiles
    """
    param = int(windows_size_for_average / 2)
    speedX = []
    speedY = []
    speedZ = []
    index_speed = []

    for i in range(len(trajectory) - 1):
        if (m.fsum(trajectory[i]) < 1e17) and (m.fsum(trajectory[i + 1]) < 1e17):  # only take the consecutive points
            speedX.append((trajectory[i + 1][0] - trajectory[i][0]) / refresh_rate)
            speedY.append((trajectory[i + 1][1] - trajectory[i][1]) / refresh_rate)
            speedZ.append((trajectory[i + 1][2] - trajectory[i][2]) / refresh_rate)
            index_speed.append(i)

    norm_speed_XY = [m.sqrt(speedX[i] ** 2 + speedY[i] ** 2) for i in range(len(speedY))]
    norm_speed_XY_SavFil = scipy.signal.savgol_filter(norm_speed_XY, savgol1, savgol2)
    norm_speed_XY_Medfilt = scipy.signal.medfilt(norm_speed_XY, medfilt)

    norm_speed_XY_mean = norm_speed_XY[:param] + [np.mean(norm_speed_XY[i - param:i + param]) for i in
                                                  range(param, len(norm_speed_XY) - param)] + norm_speed_XY[len(
        norm_speed_XY) - param:]

    return norm_speed_XY, norm_speed_XY_mean, norm_speed_XY_Medfilt, norm_speed_XY_SavFil,index_speed


def get_speed_raw_profile(trajectory, refresh_rate):
    """
    Generate the raw speed profile

    :param trajectory: the trajectory as generated by trajectory_utils.py
    :param refresh_rate: the refresh rate associate withe the trajectory
    :return: the raw speed profile and the index associate
    """
    speedX = []
    speedY = []
    speedZ = []
    index_speed = []

    for i in range(len(trajectory) - 1):
        if (m.fsum(trajectory[i]) < 1e17) and (m.fsum(trajectory[i + 1]) < 1e17):  # only take true consecutive points
            speedX.append((trajectory[i + 1][0] - trajectory[i][0]) / refresh_rate)
            speedY.append((trajectory[i + 1][1] - trajectory[i][1]) / refresh_rate)
            speedZ.append((trajectory[i + 1][2] - trajectory[i][2]) / refresh_rate)
            index_speed.append(i)

    norm_speed_XY = [m.sqrt(speedX[i] ** 2 + speedY[i] ** 2) for i in range(len(speedY))]

    return norm_speed_XY,index_speed

def export_speed_profiles(trajectory, refres_rate):
    """
    Export speed profile to png using get_speed_profiles function

    :param trajectory: the trajectory as generated by trajectory_utils.py
    :param refres_rate: the refresh rate associate withe the trajectory
    :return: None

    Note : the exports goes to the path export/profile_name_h_min_s_day_month_year.png
    """
    norm_speed_XY, norm_speed_XY_mean, norm_speed_XY_Medfilt, norm_speed_XY_SavFil, index_speed=get_speed_profiles(trajectory,refres_rate)
    pl.figure()
    pl.title('Profil de vitesse brut')
    pl.ylabel('Vitesse en m/s')
    pl.xlabel('Num de frame')
    pl.plot(index_speed, norm_speed_XY)
    pl.savefig('export/Profil_brut_' + str(time.localtime().tm_hour) + 'h_' + str(time.localtime().tm_min) + 'min_' + str(
        time.localtime().tm_sec) + 'sec_' +
               str(time.localtime().tm_mday) + '-' + str(time.localtime().tm_mon) + '-' + str(time.localtime().tm_year) + '.png')
    pl.close()
    pl.figure()
    pl.title('Profil de vitesse median')
    pl.ylabel('Vitesse en m/s')
    pl.xlabel('Num de frame')
    pl.plot(index_speed, norm_speed_XY_Medfilt)
    pl.savefig('export/Profil_median_' + str(time.localtime().tm_hour) + 'h_' + str(time.localtime().tm_min) + 'min_' + str(
        time.localtime().tm_sec) + 'sec_' +
               str(time.localtime().tm_mday) + '-' + str(time.localtime().tm_mon) + '-' + str(time.localtime().tm_year) + '.png')
    pl.close()
    pl.figure()
    pl.title('Profil de vitesse filtre')
    pl.plot(index_speed, norm_speed_XY_SavFil)
    pl.savefig('export/Profil_filtreSV_' + str(time.localtime().tm_hour) + 'h_' + str(time.localtime().tm_min) + 'min_' + str(
        time.localtime().tm_sec) + 'sec_' +
               str(time.localtime().tm_mday) + '-' + str(time.localtime().tm_mon) + '-' + str(time.localtime().tm_year) + '.png')
    pl.close()
    pl.figure()
    pl.title('profil de vitesse moyenne')
    pl.ylabel('Vitesse en m/s')
    pl.xlabel('Num de frame')
    pl.plot(index_speed, norm_speed_XY_mean)
    pl.savefig('export/Profil_moyen_' + str(time.localtime().tm_hour) + 'h_' + str(time.localtime().tm_min) + 'min_' + str(
        time.localtime().tm_sec) + 'sec_' +
               str(time.localtime().tm_mday) + '-' + str(time.localtime().tm_mon) + '-' + str(time.localtime().tm_year) + '.png')
    pl.close()
