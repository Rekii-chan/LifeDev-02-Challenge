from time import time
import inspect
import resource


class CodeBattleCore:
    def run_function(self, func, *args, **kwargs):
        """Chạy hàm được truyền vào và đo thời gian, bộ nhớ sử dụng

        :param func (function): Hàm cần chạy
        :param args: Các tham số không đặt tên
        :param kwargs: Các tham số có đặt tên

        :return (tuple): Trả về kết quả, lỗi (nếu có), thời gian thực thi và bộ nhớ sử dụng
        """

        start_time = time()
        start_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

        try:
            result = func(*args, **kwargs)
            stderr = None
        except Exception as e:
            result = None
            stderr = str(e)

        end_time = time()
        end_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

        execution_time = round(end_time - start_time, 2)
        memory_used = end_memory - start_memory

        return result, stderr, execution_time, memory_used

    def evaluate(self, func, *args, **kwargs):
        """Đánh giá hàm được truyền vào và tính điểm

        :param func (function): Hàm cần đánh giá
        :param args: Các tham số không đặt tên
        :param kwargs: Các tham số có đặt tên

        :return (dict): Trả về kết quả, lỗi (nếu có), thời gian thực thi, bộ nhớ sử dụng và điểm
        """

        result, stderr, execution_time, memory_used = self.run_function(func, *args, **kwargs)
        line_nummber = self.count_lines_of_function(func)
        score = self.custom_scoring_function(result, stderr, execution_time, memory_used, line_nummber)
        return {
            'result': result,
            'stderr': stderr,
            'execution_time': execution_time,
            'memory_used': memory_used,
            'score': score
        }

    @staticmethod
    def count_lines_of_function(func):
        """Đếm số dòng của hàm được truyền vào

        :param func (function): Hàm cần đếm số dòng

        :return (int): Trả về số dòng của hàm
        """
        source_lines, _ = inspect.getsourcelines(func)
        return len(source_lines)

    @classmethod
    def custom_scoring_function(self, result, stderr, execution_time, memory_used, line_nummber):
        """Hàm này sử dụng để tính điểm custom dựa trên kết quả, lỗi, thời gian thực thi và bộ nhớ sử dụng. NhiTX update ở đây

        :param result: Kết quả của hàm
        :param stderr: Lỗi (nếu có)
        :param execution_time (float): Thời gian thực thi
        :param memory_used (int): Bộ nhớ sử dụng
        :param line_nummber (int): Số dòng của hàm

        :return (int): Trả về điểm
        """

        if (stderr):
            return 0  # Nếu có lỗi, điểm là 0
        score = 100 - execution_time - memory_used / 1024 + line_nummber  # Ví dụ: điểm theo thời gian, số dòng và bộ nhớ sử dụng
        return max(score, 0)  # Điểm không thể âm


if __name__ == '__main__':
    # Sử dụng core
    code_battle_core = CodeBattleCore()

    def sample_function(n):
        total = 0
        for i in range(n):
            total += i
        return total

    result = code_battle_core.evaluate(sample_function, 1000000)
    for k, v in result.items():
        print(k, ":", v)
    print("\nNumber of lines in sample_function:", CodeBattleCore.count_lines_of_function(sample_function))
