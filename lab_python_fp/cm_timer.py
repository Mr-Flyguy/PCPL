import time
import contextlib

class cm_timer_1:
    
    def __enter__(self):
        self.start = time.time()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        end_time = time.time()
        elapsed_time = end_time - self.start
        print(f'time: {elapsed_time:.1f}')
        
@contextlib.contextmanager
def cm_timer_2():
    start_time = time.time()
    yield
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f'time: {elapsed_time:.1f}')
    
if __name__ == '__main__':
    with cm_timer_1():
        time.sleep(5.5)
        
    with cm_timer_2():
        time.sleep(5.5)