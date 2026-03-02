import os

import square
import circle

def main():
    side = float(os.environ['SQUARE_SIDE'])
    radius = float(os.environ['CIRCLE_RADIUS'])

    print(f"square area: {square.area(side)}, perimeter: {square.perimeter(side)}")
    print(f"circle area: {circle.area(radius)}, perimeter: {circle.perimeter(radius)}")

if __name__ == "__main__":
    main()