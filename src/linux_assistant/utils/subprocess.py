import subprocess
import tempfile
import io, os
import threading

class processor:
    def __init__(self, show_output=False):
        self.output = {'stderr':None, "stdout":None, "returncode":None}
        self.show_output = show_output

    def sucprocess(self, code):
        path = self.create_tmp_file(code)
        returncode, stdout, stderr = self.run_interactive_subprocess(['bash', path])
        os.remove(path)
        self.output = {'stderr':stderr, "stdout":stdout, "returncode":returncode}
        
    def run_interactive_subprocess(self, command):

        stdout_buffer = io.StringIO()
        stderr_buffer = io.StringIO()
        
        try:
            process = subprocess.Popen(
                command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            
            stdout_thread = threading.Thread(
                target=self.read_output, 
                args=(process.stdout, "Subprocess output", stdout_buffer, self.show_output)
            )
            stderr_thread = threading.Thread(
                target=self.read_output, 
                args=(process.stderr, "Subprocess error", stderr_buffer, self.show_output)
            )
            
            stdout_thread.daemon = True
            stderr_thread.daemon = True
            
            stdout_thread.start()
            stderr_thread.start()
            
            process.stdin.close()  
            
            returncode = process.wait()
            
            stdout_thread.join(timeout=1)
            stderr_thread.join(timeout=1)
            
            stdout_content = stdout_buffer.getvalue()
            stderr_content = stderr_buffer.getvalue()

            return returncode, stdout_content, stderr_content
            
        except Exception as e:
            print(f"Error: {e}")
            return -1, "", str(e)
        
    @staticmethod
    def create_tmp_file(code):
        with tempfile.NamedTemporaryFile("w", suffix=".sh", delete=False) as tf:
            tf.write(code)
            path = tf.name
        return path
        
    @staticmethod
    def read_output(stream, prefix, buffer, show_output=True):
            while True:
                line = stream.readline()
                if not line:
                    break
                if show_output:
                    print(f"{prefix}: {line.strip()}")
                buffer.write(line)