from analyser.core import ULog
import analyser.ulog2csv as ulg2csv

class UlogConverter:

    def show_info(self, ulog):
        data_list_sorted = sorted(ulog.data_list, key=lambda d: d.name + str(d.multi_id))
        nameList = []
        for d in data_list_sorted:
            name_id = "{:}".format(d.name)
            nameList.append(name_id)
        return nameList

    def ulogToCSV(self, log_path, file_path):
        messages = self.show_info(ULog(file_path, None, None))
        ulg2csv.convert_ulog2csv(file_path, messages, log_path, ',')

        return