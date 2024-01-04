import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, CheckButtons, Button
from scipy import signal

# Початкові параметри
initial_amplitude = 1.0
initial_frequency = 1.0
initial_phase = 0.0
initial_noise_mean = 0.0
initial_noise_covariance = 0.1

# Генерація  вектора
t = np.linspace(0, 10, 1000, endpoint=False)

# Створення фігури та осей
fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(left=0.2, right=0.8)

# Функція гармоніки з шумом
def harmonic_with_noise(amplitude, frequency, phase, noise_mean, noise_covariance, show_noise):
    signal_without_noise = amplitude * np.sin(2 * np.pi * frequency * t + phase)
    if show_noise:
        noise = np.random.normal(noise_mean, np.sqrt(noise_covariance), len(t))
        return signal_without_noise + noise
    else:
        return signal_without_noise

# Лінії для графіків
line_original, = ax.plot(t, harmonic_with_noise(initial_amplitude, initial_frequency, initial_phase,
                                                 initial_noise_mean, initial_noise_covariance, True), lw=2)
line_filtered, = ax.plot(t, harmonic_with_noise(initial_amplitude, initial_frequency, initial_phase,
                                                 initial_noise_mean, initial_noise_covariance, True), lw=2, linestyle='dashed')

# Створення слайдерів
ax_amplitude = plt.axes([0.2, 0.01, 0.65, 0.03])
ax_frequency = plt.axes([0.2, 0.06, 0.65, 0.03])
ax_phase = plt.axes([0.2, 0.11, 0.65, 0.03])
ax_noise_mean = plt.axes([0.2, 0.16, 0.65, 0.03])
ax_noise_covariance = plt.axes([0.2, 0.21, 0.65, 0.03])

s_amplitude = Slider(ax_amplitude, 'Амплітуда', 0.1, 2.0, valinit=initial_amplitude)
s_frequency = Slider(ax_frequency, 'Частота', 0.1, 10.0, valinit=initial_frequency)
s_phase = Slider(ax_phase, 'Фазовий зсув', 0.0, 2 * np.pi, valinit=initial_phase)
s_noise_mean = Slider(ax_noise_mean, 'Середнє значення шуму', -1.0, 1.0, valinit=initial_noise_mean)
s_noise_covariance = Slider(ax_noise_covariance, 'Дисперсія шуму', 0.01, 1.0, valinit=initial_noise_covariance)

# Чекбокс для перемикання відображення шуму
ax_show_noise = plt.axes([0.85, 0.15, 0.1, 0.1])
check_button = CheckButtons(ax_show_noise, ['Відображати шум'], [True])


# Функція для фільтрації сигналу
def filter_signal(signal_data):
    b, a = signal.butter(4, 0.1, 'low')
    filtered_signal = signal.filtfilt(b, a, signal_data)
    return filtered_signal

# Функція для оновлення графіку

def update_and_filter(val):
    amplitude = s_amplitude.val
    frequency = s_frequency.val
    phase = s_phase.val
    noise_mean = s_noise_mean.val
    noise_covariance = s_noise_covariance.val
    show_noise = check_button.get_status()[0]

    # Оновлення значень первинної гармоніки
    line_original.set_ydata(harmonic_with_noise(amplitude, frequency, phase, noise_mean, noise_covariance, show_noise))

    # Фільтрація та оновлення фільтрованої гармоніки
    filtered_signal = filter_signal(line_original.get_ydata())
    line_filtered.set_ydata(filtered_signal)

    # Оновлення графіку
    fig.canvas.draw_idle()


# Підключення функції до слайдерів та чекбокса
s_amplitude.on_changed(update_and_filter)
s_frequency.on_changed(update_and_filter)
s_phase.on_changed(update_and_filter)
s_noise_mean.on_changed(update_and_filter)
s_noise_covariance.on_changed(update_and_filter)
check_button.on_clicked(update_and_filter)


# Кнопка для скидання параметрів
ax_reset = plt.axes([0.85, 0.06, 0.1, 0.04])
reset_button = Button(ax_reset, 'Reset', color='lightgoldenrodyellow', hovercolor='0.975')

def reset(event):
    s_amplitude.reset()
    s_frequency.reset()
    s_phase.reset()
    s_noise_mean.reset()
    s_noise_covariance.reset()

reset_button.on_clicked(reset)

# Кнопка для включення/виключення відображення відфільтрованої гармоніки
ax_toggle_filtered = plt.axes([0.85, 0.21, 0.1, 0.04])
toggle_filtered_button = Button(ax_toggle_filtered, 'Відобразити фільтровану', color='lightgoldenrodyellow', hovercolor='0.975')

def toggle_filtered(event):
    line_filtered.set_visible(not line_filtered.get_visible())
    fig.canvas.draw_idle()

toggle_filtered_button.on_clicked(toggle_filtered)

# Кнопка для включення/виключення відображення початкової гармоніки
ax_toggle_original = plt.axes([0.85, 0.26, 0.1, 0.04])
toggle_original_button = Button(ax_toggle_original, 'Відобразити початкову', color='lightgoldenrodyellow', hovercolor='0.975')
def toggle_original(event):
    line_original.set_visible(not line_original.get_visible())
    fig.canvas.draw_idle()

toggle_original_button.on_clicked(toggle_original)

# Додайте легенду
ax.legend()

# Відображення графічного інтерфейсу
plt.show()
