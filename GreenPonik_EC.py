import time
import requests

_kvalue = 1.0
_kvalueLow = 1.0
_kvalueHigh = 1.0
_voltage = 0.0
_temperature = 25.0

_raw_1413 = 1.200
_raw_1413_offset = 0.750
_raw_276 = 2.500
_raw_276_offset_low = 0.500
_raw_276_offset_high = 1.000
_raw_1288 = 11.850
_raw_1288_offset = 3.650

TXT_FILE_PATH = "~/sistachansen/GreenPonik_EC_Python_industrial_probes/example/"

def upload_file_to_website(file_path):
    url = 'https://quorkel.com/iot/group15/ec_readings.txt'
    with open(file_path, 'rb') as file:
        response = requests.post(url, files={'file': file})
#    if response.status_code == 200:
#        print("File uploaded successfully.")
#    else:
 #       print("File upload failed.")


class GreenPonik_EC():
    def begin(self):
        global _kvalueLow
        global _kvalueHigh
        try:
#            print(">>>Initialization of ec lib<<<")
            with open('ecdata.txt', 'r') as f:
                kvalueLowLine = f.readline()
                kvalueLowLine = kvalueLowLine.strip('kvalueLow=')
                _kvalueLow = float(kvalueLowLine)
 #               print("get k value low from txt file: %.3f" % _kvalueLow)
                kvalueHighLine = f.readline()
  #              kvalueHighLine = kvalueHighLine.strip('kvalueHigh=')
                _kvalueHigh = float(kvalueHighLine)
  #              print("get k value high from txt file: %.3f" % _kvalueHigh)
        except:
            self.reset()

    def readEC(self, voltage, temperature):
        global _kvalueLow
        global _kvalueHigh
        global _kvalue
        #        print(">>>current voltage is: %.3f mV" % voltage)
        rawEC = 1000 * voltage / (7500 / 0.66) / 20 * 10 * 2.2
        #       print(">>>current rawEC is: %.3f" % rawEC)
        # a = (Y2-Y1)/(X2-X1)
        slope = (_kvalueHigh - _kvalueLow) / (2.76 - 1.413)
        # b = Y1 - (a*X1)
        intercept = _kvalueLow - (slope * 1.413)
        _kvalue = (slope * rawEC) + intercept
        #        print(">>>interpolated _kvalue: %.5f" % _kvalue)
        value = rawEC * _kvalue
        value = value / (1.0 + 0.0185 * (temperature - 25.0))
        print(">>>interpolated EC: %.5f" % value)
        with open('ec_readings.txt', 'a') as f:  # Open the file in append mode
            # Write the EC and temperature values to the file
            f.write("Temperature: %.2f, EC: %.3f\n" % (temperature, value))

        # Upload the updated file to the website
        upload_file_to_website('ec_readings.txt')

        return value

    def KvalueTempCalculation(self, compECsolution, voltage):
        return 820.0 * 200.0 * compECsolution

    def calibration(self, voltage, temperature):
        rawEC = 1000 * voltage / 820.0 / 200.0
        print(">>>current rawEC is: %.3f" % rawEC)

        if rawEC > _raw_1413 - _raw_1413_offset and rawEC < _raw_1413 + _raw_1413_offset:
            compECsolution = 1.413 * (1.0 + 0.0185 * (temperature - 25.0))
            KValueTemp = self.KvalueTempCalculation(compECsolution, voltage)
            KValueTemp = round(KValueTemp, 2)
            print(">>>Buffer Solution:1.413us/cm")
            f = open('ecdata.txt', 'r+')
            flist = f.readlines()
            flist[0] = 'kvalueLow=' + str(KValueTemp) + '\n'
            f = open('ecdata.txt', 'w+')
            f.writelines(flist)
            f.close()
            status_msg = ">>>EC:1.413us/cm Calibration completed<<<"
            print(status_msg)
            time.sleep(5.0)
            cal_res = {'status': 1413, 'kvalue': KValueTemp, 'status_message': status_msg}
            return cal_res

        elif rawEC > _raw_276 - _raw_276_offset_low and rawEC < _raw_276 + _raw_276_offset_h >
            compECsolution = 2.76 * (1.0 + 0.0185 * (temperature - 25.0))
            KValueTemp = self.KvalueTempCalculation(compECsolution, voltage)
            KValueTemp = round(KValueTemp, 2)
            print(">>>Buffer Solution:2.76ms/cm")
            f = open('ecdata.txt', 'r+')
            flist = f.readlines()
            flist[1] = 'kvalueHigh=' + str(KValueTemp) + '\n'
            f = open('ecdata.txt', 'w+')
            f.writelines(flist)
            f.close()
            status_msg = ">>>EC:2.76ms/cm Calibration completed<<<"
            print(status_msg)
            time.sleep(5.0)
            cal_res = {'status': 276, 'kvalue': KValueTemp, 'status_message': status_msg}
            return cal_res

        elif rawEC > _raw_1288 - _raw_1288_offset and rawEC < _raw_1288 + _raw_1288_offset:
            compECsolution = 12.88 * (1.0 + 0.0185 * (temperature - 25.0))
            KValueTemp = self.KvalueTempCalculation(compECsolution, voltage)
            KValueTemp = round(KValueTemp, 2)
            print(">>>Buffer Solution:12.88ms/cm")
            f = open('ecdata.txt', 'r+')
            flist = f.readlines()
            flist[2] = 'kvalue=' + str(KValueTemp) + '\n'
            f = open('ecdata.txt', 'w+')
            f.writelines(flist)
            f.close()
            status_msg = ">>>EC:12.88ms/cm Calibration completed<<<"
            print(status_msg)
            time.sleep(5.0)
            cal_res = {'status': 1288, 'kvalue': KValueTemp, 'status_message': status_msg}
            return cal_res

        else:
            status_msg = ">>>Buffer Solution Error, EC raw: %.3f, Try Again<<<" % rawEC
            print(status_msg)
            cal_res = {'status': 9999, 'status_message': status_msg}
            return cal_res

    def reset(self):
        global _kvalueLow
        global _kvalueHigh
        _kvalueLow = 1.0
        _kvalueHigh = 1.0
        print(">>>Reset to default parameters<<<")
        try:
            print(">>>Read k from txt files<<<")
            f = open('ecdata.txt', 'r+')
            flist = f.readlines()
            flist[0] = 'kvalueLow=' + str(_kvalueLow) + '\n'
            flist[1] = 'kvalueHigh=' + str(_kvalueHigh) + '\n'
            f = open('ecdata.txt', 'w+')
            f.writelines(flist)
            f.close()
        except:
        print(">>>Cannot read k from txt files<<<")
        print(">>>Let's create them and apply the default values<<<")
        f = open('ecdata.txt', 'w')
        flist = 'kvalueLow=' + str(_kvalueLow) + '\n'
        flist += 'kvalueHigh=' + str(_kvalueHigh) + '\n'
        f.writelines(flist)
        f.close()




