def draw_plot(canvas, actual, predicted):
    canvas.delete("all")
    draw_lines(canvas, actual, 'blue', 0)
    draw_lines(canvas, predicted, 'red', 5)

def draw_lines(canvas, data, color, offset=0):
    max_val = max(max(data), 1)
    min_val = min(min(data), 0)
    scaled_data = [(x - min_val) / (max_val - min_val) * 300 for x in data]

    for i in range(len(scaled_data) - 1):
        canvas.create_line(50 * i + 20 + offset, 350 - scaled_data[i],
                           50 * (i + 1) + 20 + offset, 350 - scaled_data[i + 1], fill=color)
