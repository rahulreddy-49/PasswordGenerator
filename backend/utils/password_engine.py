import random
import string
import math
from zxcvbn import zxcvbn

class PasswordEngine:
    @staticmethod
    def generate(length=16, use_upper=True, use_lower=True, use_digits=True, use_symbols=True):
        """Generates a secure random password."""
        chars = ""
        if use_upper: chars += string.ascii_uppercase
        if use_lower: chars += string.ascii_lowercase
        if use_digits: chars += string.digits
        if use_symbols: chars += string.punctuation

        if not chars:
            chars = string.ascii_letters + string.digits

        password = "".join(random.SystemRandom().choice(chars) for _ in range(length))
        return password

    @staticmethod
    def analyze(password):
        """Analyzes password strength using zxcvbn and entropy calculations."""
        # zxcvbn analysis
        results = zxcvbn(password)
        score = results['score']  # 0 to 4
        crack_times = results['crack_times_display']['offline_slow_hashing_1e4_per_second']
        
        # Entropy calculation
        charset_size = 0
        if any(c.islower() for c in password): charset_size += 26
        if any(c.isupper() for c in password): charset_size += 26
        if any(c.isdigit() for c in password): charset_size += 10
        if any(c in string.punctuation for c in password): charset_size += 32
        
        entropy = 0
        if charset_size > 0:
            entropy = math.log2(charset_size) * len(password)

        return {
            "score": score,
            "entropy": round(entropy, 2),
            "crack_time": crack_times,
            "suggestions": results['feedback']['suggestions'],
            "warning": results['feedback']['warning']
        }
