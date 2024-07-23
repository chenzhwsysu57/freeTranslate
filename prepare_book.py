# 这段代码从给定的latex文件对教材进行截断。
# 每5000字为一段，但是按照section截取。
# 截断的结果，返回

def make_datasets(sections):
    datasets = []
    current_set = " "
    current_len = 0

    for section in sections:
        
        
        if len(section) + current_len <= 5000:
            current_set += str(section)
            current_len += len(section)
        else:
            datasets.append(current_set)
            current_set = " " + section
            current_len = len(section)

    if current_set:
        datasets.append(current_set)

    return datasets
