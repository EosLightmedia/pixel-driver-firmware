import gc

try:
    from ulab import numpy as np
    u = True
except ImportError:
    import numpy as np
    import scipy as sp
    u = False

class CNDL:
    version = '1.0.0'
    
    def __init__(self, cndl_code: str):        
        print(f'Parsing CNDL code...\n{cndl_code}\n\n')
        if '/SET' not in cndl_code:
            raise SyntaxError('CNDL script must contain a SET block')
        if '/DEF' not in cndl_code:
            raise SyntaxError('CNDL script must contain a DEF block')
        if '/RUN' not in cndl_code:
            raise SyntaxError('CNDL script must contain a RUN block')
        if '/OUT' not in cndl_code:
            raise SyntaxError('CNDL script must contain an OUT block')
        
        _ , _code = cndl_code.strip().split('/SET')
        set_code, _code = _code.strip().split('/DEF')
        def_code, _code = _code.strip().split('/RUN')
        run_code, out_code = _code.strip().split('/OUT')

        set_lines = [line.strip() for line in set_code.splitlines() if line.strip()]
        def_lines = [line.strip() for line in def_code.splitlines() if line.strip()]
        run_lines = [line.strip() for line in run_code.splitlines() if line.strip()]
        out_lines = [line.strip() for line in out_code.splitlines() if line.strip()]
        
        self.layers_per_pixel = len(out_lines)
        
        self.global_vars = dict()
        self.global_vars['WIDTH'] = 1
        self.global_vars['HEIGHT'] = 1
        self.global_vars['BRIGHTNESS'] = 1.0
        self.global_vars['DELTA'] = 0.16
        self.global_vars['IN1'] = 0.
        self.global_vars['IN2'] = 0.
        self.global_vars['pi'] = np.pi
        self.global_vars['e'] = np.e
        self.global_vars['sin'] = self._sin
        self.global_vars['cos'] = self._cos
        self.global_vars['pos'] = self._pos
        self.global_vars['abs'] = self._abs
        self.global_vars['map'] = self._map
        
        for set_line in set_lines:
            variable, expression = set_line.split(' ')
            self.global_vars[variable] = eval(expression)
        
        print(f'Allocating: output-buffer of size {self.global_vars["WIDTH"]}x{self.global_vars["HEIGHT"]}x{self.layers_per_pixel}')
        self.output_buffer = np.zeros((self.global_vars['HEIGHT'], self.global_vars['WIDTH'], self.layers_per_pixel))
        
        self.local_vars: dict[str, np.ndarray] = dict()
        
        print(f'Generating X and Y values')
        self.local_vars['X'], self.local_vars['Y'] = self.generate_uv(self.global_vars['WIDTH'], self.global_vars['HEIGHT'])
        
        self.blanking_zero: list[np.ndarray] = []
        self.blanking_clip: list[np.ndarray] = []
        self.blanking_wrap: list[np.ndarray] = []
        self.blanking_snow: list[np.ndarray] = []
        self.blanking_rand: list[np.ndarray] = []
            
        for def_line in def_lines:
            blanking_operation, variable_name = def_line.split(' ')
            print(f'Allocating: {variable_name}')
            new_tensor = np.zeros((self.global_vars['HEIGHT'], self.global_vars['WIDTH']))
            self.local_vars[variable_name] = new_tensor
            if blanking_operation == 'ZERO':
                self.blanking_zero.append(new_tensor)
            elif blanking_operation == 'CLIP':
                self.blanking_clip.append(new_tensor)
            elif blanking_operation == 'WRAP':
                self.blanking_wrap.append(new_tensor)
            elif blanking_operation == 'SNOW':
                self.blanking_snow.append(new_tensor)
            elif blanking_operation == 'RAND':
                self.blanking_rand.append(new_tensor)
            else:
                raise SyntaxError(f'Unknown blanking operation: {blanking_operation} in line: {def_line}')
            
        
        self.run_operations: list[tuple[callable, np.ndarray, str]] = []
        
        for run_line in run_lines:
            operation, variable_name, expression = run_line.split(' ', 2)
            
            if not variable_name in self.local_vars:
                raise SyntaxError(f'Unknown variable name \"{variable_name}\" from line: {run_line}')
            
            try:
                eval(expression, self.global_vars, self.local_vars)
            except Exception as e:
                raise SyntaxError(f'{e} from line: {run_line}')
            
            if operation == 'MOVE':
                self.run_operations.append((self._MOVE, self.local_vars[variable_name], expression))
            elif operation == 'SIZE':
                self.run_operations.append((self._SIZE, self.local_vars[variable_name], expression))
            elif operation == 'CFFT':
                self.run_operations.append((self._CFFT, self.local_vars[variable_name], expression))
            else:
                raise SyntaxError(f'Unknown operation \"{operation}\" from line: {run_line}')

        self.output_evaluations: list[str] = []

        for out_line in out_lines:
            try:
                eval(out_line, self.global_vars, self.local_vars)
            except Exception as e:
                raise SyntaxError(f'{e} from line: {out_line}')
            
            self.output_evaluations.append(out_line)
        
        self.eval = eval
        gc.collect()
        
    @staticmethod
    def _MOVE(tensor: np.ndarray, value: np.ndarray | float):
        tensor += value
        
    @staticmethod
    def _SIZE(tensor: np.ndarray, value: np.ndarray | float):
        tensor *= value
    
    @staticmethod
    def _CFFT(tensor: np.ndarray, value: np.ndarray):
        if u:
            raise NotImplementedError('NOT COMPATIBLE WITH PIXEL DRIVER')
        tensor[:] = sp.signal.fftconvolve(tensor, value, mode='same')

    @staticmethod
    def _sin(value: np.ndarray | float):
        return np.sin(value)
    
    @staticmethod
    def _cos(value: np.ndarray | float):
        return np.cos(value)
    
    @staticmethod
    def _pos(value: np.ndarray | float):
        return np.where(value > 0., value, 0.)
    
    @staticmethod
    def _abs(value: np.ndarray | float):
        return np.abs(value)
    
    @staticmethod
    def _map(value: np.ndarray | float):
        return (value + 1.) / 2.

    @staticmethod
    def generate_uv(width, height):
        x = np.zeros((height, width))
        y = np.zeros((height, width))
    
        if width > 1 and height > 1:
            for i in range(height):
                for j in range(width):
                    x[i, j] = -1 + 2 * j / (width - 1)
                    y[i, j] = -1 + 2 * (height - 1 - i) / (height - 1)
    
        elif width == 1 and height > 1:
            for i in range(height):
                y[i, 0] = -1 + 2 * (height - 1 - i) / (height - 1)
                x[:, 0] = 0
    
        elif height == 1 and width > 1:
            for j in range(width):
                x[0, j] = -1 + 2 * j / (width - 1)
                y[0, :] = 0
        else:
            x[0, 0] = 0
            y[0, 0] = 0
    
        return x, y

    def update(self, delta: float, in_1: float, in_2: float):
        self.global_vars['IN1'] = in_1
        self.global_vars['IN2'] = in_2
        self.global_vars['DELTA'] = delta
        
        for tensor in self.blanking_zero:
            tensor *= 0.
        for tensor in self.blanking_clip:
            tensor[:] = np.clip(tensor, -1, 1)
        for tensor in self.blanking_wrap:
            tensor -= ((tensor + 1.) // 2.) * 2.
        for tensor in self.blanking_rand:
            tensor += np.random.uniform(-1, 1, (1, 1))
        for tensor in self.blanking_snow:
            tensor[:] = np.random.uniform(-1, 1, tensor.shape)
        
        for operation, tensor, expression in self.run_operations:
            operation(tensor, self.eval(expression, self.global_vars, self.local_vars))

        for i, out_eval in enumerate(self.output_evaluations):
            self.output_buffer[:, :, i] = self.eval(out_eval, self.global_vars, self.local_vars)
        
        return np.clip(self.output_buffer, 0., 1.)
