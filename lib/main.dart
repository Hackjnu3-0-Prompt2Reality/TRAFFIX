import 'dart:async';
import 'dart:io';
import 'dart:math';
import 'package:flutter/material.dart';

void main() {
  runApp(MyApp());
}

class RoadSimulator extends StatefulWidget {
  @override
  _RoadSimulatorState createState() => _RoadSimulatorState();
}

class _RoadSimulatorState extends State<RoadSimulator> {
  int activeLightIndex = 0;
  List<bool> redLights = [true, true, true, true];
  List<Car> horizontal1Cars = [];
  List<Car> horizontal2Cars = [];
  List<Car> vertical1Cars = [];
  List<Car> vertical2Cars = [];

  @override
  void initState() {
    super.initState();

    // Add more cars to the horizontal road
    for (int i = 0; i < 20; i++) {
      horizontal1Cars.add(Car(lane: i % 5, lane2: i % 3, lane3: i % 2, position: i.toDouble() * 30.0, isHorizontal: true));
    }
    for (int i = 0; i < 20; i++) {
      horizontal2Cars.add(Car(lane: i % 1, lane2: i % 2, lane3: i % 3, position: i.toDouble() * 30.0, isHorizontal: true));
    }

    // Add more cars to the vertical road with random lanes
    for (int i = 0; i < 20; i++) {
      vertical1Cars.add(Car(lane: Random().nextInt(3), lane2: i % 5, lane3: i % 3, position: i.toDouble() * 30.0, isHorizontal: false));
    }
    for (int i = 0; i < 20; i++) {
      vertical2Cars.add(Car(lane: Random().nextInt(3), lane2: i % 4, lane3: i % 1, position: i.toDouble() * 30.0, isHorizontal: false));
    }

    // Timer to control traffic light changes
    Timer.periodic(Duration(seconds: 30), (timer) {
      setState(() {
        redLights[activeLightIndex] = true;
        activeLightIndex = (activeLightIndex + 1) % 4;
        redLights[activeLightIndex] = false;
      });
    });

    // Periodically update car positions
    Timer.periodic(Duration(milliseconds: 50), (timer) {
      setState(() {
        for (var car in horizontal1Cars) {
          if (!redLights[0]) {
            car.move(true);
          }
        }
        for (var car in horizontal2Cars) {
          if (!redLights[1]) {
            car.move(true);
          }
        }
        for (var car in vertical1Cars) {
          if (!redLights[2]) {
            car.move(false);
          }
        }
        for (var car in vertical2Cars) {
          if (!redLights[3]) {
            car.move(false);
          }
        }
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          title: Text('Traffic Simulation'),
        ),
        body: ListView(
          children: [
            Flexible(
              child: Container(
                width: double.maxFinite,
                decoration: BoxDecoration(
                  gradient: LinearGradient(
                    begin: Alignment.topCenter,
                    end: Alignment.bottomCenter,
                    colors: [Color(0xFF87CEEB), Color(0xFF00FF00)],
                    stops: [0.6, 1.0],
                  ),
                ),
                child: Column(
                  children: [
                    Row(
                      children: [
                        Column(
                          children: [
                            Row(children: [
                              // Horizontal Road with Cars and Traffic Light
                              Container(
                                width: 400,
                                height: 200,
                                decoration: BoxDecoration(
                                  gradient: LinearGradient(
                                    begin: Alignment.centerRight,
                                    end: Alignment.centerLeft,
                                    colors: [Colors.red, Colors.blue],
                                  ),
                                  border: Border.all(color: Colors.black),
                                ),
                                child: Align(
                                  alignment: Alignment.center,
                                  child: Stack(
                                    children: horizontal1Cars.map((car) {
                                      return Positioned(
                                        left: car.position,
                                        top: car.lane * 200.0 + (car.lane2 * 100) - (car.lane3 * 50),
                                        child: Container(
                                          width: 30,
                                          height: 20,
                                          child: RealisticCar(),
                                        ),
                                      );
                                    }).toList(),
                                  ),
                                ),
                              ),
                              GestureDetector(
                                onTap: () => toggleTrafficLight(0),
                                child: Container(
                                  width: 25,
                                  height: 75,
                                  color: redLights[0] ? Colors.red : Colors.green,
                                ),
                              ),
                            ]),
                            Row(children: [
                              Container(
                                width: 400,
                                height: 200,
                                decoration: BoxDecoration(
                                  gradient: LinearGradient(
                                    begin: Alignment.centerRight,
                                    end: Alignment.centerLeft,
                                    colors: [Colors.red, Colors.blue],
                                  ),
                                  border: Border.all(color: Colors.black),
                                ),
                                child: Align(
                                  alignment: Alignment.center,
                                  child: Stack(
                                    children: horizontal2Cars.map((car) {
                                      return Positioned(
                                        right: car.position,
                                        top: car.lane * 200.0 + (car.lane2 * 100) - (car.lane3 * 50),
                                        child: Container(
                                          width: 30,
                                          height: 20,
                                          child: RealisticCar(),
                                        ),
                                      );
                                    }).toList(),
                                  ),
                                ),
                              ),
                              GestureDetector(
                                onTap: () => toggleTrafficLight(1),
                                child: Container(
                                  width: 25,
                                  height: 75,
                                  color: redLights[1] ? Colors.red : Colors.green,
                                ),
                              ),
                            ]),
                          ],
                        ),
                        Column(
                          children: [
                            Row(children: [
                              Column(children: [
                                // Vertical Road with Cars and Traffic Light
                                Container(
                                  width: 200,
                                  height: 400,
                                  decoration: BoxDecoration(
                                    border: Border.all(color: Colors.black),
                                    gradient: LinearGradient(
                                      begin: Alignment.centerRight,
                                      end: Alignment.centerLeft,
                                      colors: [Colors.red, Colors.blue],
                                    ),
                                  ),
                                  child: Align(
                                    alignment: Alignment.center,
                                    child: Stack(
                                      children: vertical1Cars.map((car) {
                                        return Positioned(
                                          left: car.lane * 200.0 + (car.lane2 * 100),
                                          top: 600 - car.position - 20 - (car.lane3 * 50),
                                          child: Container(
                                            width: 30,
                                            height: 20,
                                            child: RealisticCar(),
                                          ),
                                        );
                                      }).toList(),
                                    ),
                                  ),
                                ),
                                GestureDetector(
                                  onTap: () => toggleTrafficLight(2),
                                  child: Container(
                                    width: 75,
                                    height: 25,
                                    color: redLights[2] ? Colors.red : Colors.green,
                                  ),
                                ),
                              ]),
                              Column(children: [
                                // Vertical Road with Cars and Traffic Light
                                Container(
                                  width: 200,
                                  height: 400,
                                  decoration: BoxDecoration(
                                    border: Border.all(color: Colors.black),
                                    gradient: LinearGradient(
                                      begin: Alignment.centerRight,
                                      end: Alignment.centerLeft,
                                      colors: [Colors.red, Colors.blue],
                                    ),
                                  ),
                                  child: Align(
                                    alignment: Alignment.center,
                                    child: Stack(
                                      children: vertical2Cars.map((car) {
                                        return Positioned(
                                          left: car.lane * 200.0 + (car.lane2 * 100),
                                          bottom: 600 - car.position - 20 - (car.lane3 * 50),
                                          child: Container(
                                            width: 30,
                                            height: 20,
                                            child: RealisticCar(),
                                          ),
                                        );
                                      }).toList(),
                                    ),
                                  ),
                                ),
                                GestureDetector(
                                  onTap: () => toggleTrafficLight(3),
                                  child: Container(
                                    width: 75,
                                    height: 25,
                                    color: redLights[3] ? Colors.red : Colors.green,
                                  ),
                                ),
                              ]),
                            ]),
                            Row(
                              children: [
                                Column(
                                  mainAxisAlignment: MainAxisAlignment.end,
                                  children: [
                                    SizedBox(
                                      height: 400,
                                      width: 420,
                                      child: Container(color: Color(0xFF87CEEB)),
                                    ),
                                  ],
                                ),
                              ],
                            ),
                            Row(children: [
                              Column(children: [
                                // Vertical Road with Cars and Traffic Light
                                Container(
                                  width: 200,
                                  height: 400,
                                  decoration: BoxDecoration(
                                    border: Border.all(color: Colors.black),
                                    gradient: LinearGradient(
                                      begin: Alignment.centerRight,
                                      end: Alignment.centerLeft,
                                      colors: [Colors.red, Colors.blue],
                                    ),
                                  ),
                                  child: Align(
                                    alignment: Alignment.center,
                                    child: Stack(
                                      children: vertical1Cars.map((car) {
                                        return Positioned(
                                          left: car.lane * 200.0 + (car.lane2 * 100),
                                          top: 600 - car.position - 20 - (car.lane3 * 50),
                                          child: Container(
                                            width: 30,
                                            height: 20,
                                            child: RealisticCar(),
                                          ),
                                        );
                                      }).toList(),
                                    ),
                                  ),
                                ),
                              ]),
                              Column(children: [
                                Container(
                                  width: 200,
                                  height: 400,
                                  decoration: BoxDecoration(
                                    border: Border.all(color: Colors.black),
                                    gradient: LinearGradient(
                                      begin: Alignment(0, 5),
                                      end: Alignment(6, 10),
                                      colors: [Colors.red, Colors.blue],
                                    ),
                                  ),
                                  child: Align(
                                    alignment: Alignment.center,
                                    child: Stack(
                                      children: vertical2Cars.map((car) {
                                        return Positioned(
                                          left: car.lane * 200.0 + (car.lane2 * 100),
                                          bottom: 600 - car.position - 20 - (car.lane3 * 50),
                                          child: Container(
                                            width: 30,
                                            height: 20,
                                            child: RealisticCar(),
                                          ),
                                        );
                                      }).toList(),
                                    ),
                                  ),
                                ),
                              ]),
                            ]),
                          ],
                        ),
                        Column(
                          children: [
                            Row(children: [
                              // Horizontal Road with Cars and Traffic Light
                              Container(
                                width: 600,
                                height: 200,
                                decoration: BoxDecoration(
                                  border: Border.all(color: Colors.black),
                                  gradient: LinearGradient(
                                    begin: Alignment.centerRight,
                                    end: Alignment.centerLeft,
                                    colors: [Colors.blue, Colors.red],
                                  ),
                                ),
                                child: Align(
                                  alignment: Alignment.center,
                                  child: Stack(
                                    children: horizontal1Cars.map((car) {
                                      return Positioned(
                                        left: car.position,
                                        top: car.lane * 200.0 + (car.lane2 * 100) - (car.lane3 * 50),
                                        child: Container(
                                          width: 30,
                                          height: 20,
                                          child: RealisticCar(),
                                        ),
                                      );
                                    }).toList(),
                                  ),
                                ),
                              ),
                            ]),
                            Row(children: [
                              Container(
                                width: 600,
                                height: 200,
                                decoration: BoxDecoration(
                                  border: Border.all(color: Colors.black),
                                  gradient: LinearGradient(
                                    begin: Alignment.centerRight,
                                    end: Alignment.centerLeft,
                                    colors: [Colors.blue, Colors.red],
                                  ),
                                ),
                                child: Align(
                                  alignment: Alignment.center,
                                  child: Stack(
                                    children: horizontal2Cars.map((car) {
                                      return Positioned(
                                        right: car.position,
                                        top: car.lane * 200.0 + (car.lane2 * 100) - (car.lane3 * 50),
                                        child: Container(
                                          width: 30,
                                          height: 20,
                                          child: RealisticCar(),
                                        ),
                                      );
                                    }).toList(),
                                  ),
                                ),
                              ),
                            ]),
                          ],
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class Car {
  double position;
  int lane;
  int lane2;
  int lane3;
  double speed;
  bool isHorizontal;

  Car({required this.position, required this.lane, required this.lane2, required this.lane3, this.speed = 4.0, required this.isHorizontal});

  void move(bool isHorizontalRoad) {
    if (isHorizontalRoad) {
      position += speed;
      if (position > 600) {
        position = 0.0;
      }
    } else {
      position += speed;
      if (position > 600) {
        position = 0.0;
        lane = Random().nextInt(3 + 8);
        lane2 = Random().nextInt(5 + 8);
        lane3 = Random().nextInt(5 + 7);
      }
    }
  }
}

class RealisticCar extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Image.network(
      "https://cdni.autocarindia.com/utils/imageresizer.ashx?n=https://cms.haymarketindia.net/model/uploads/modelimages/Lamborghini-Revuelto-190920231426.jpg&w=872&h=578&q=75&c=1",
    );
  }
}

void toggleTrafficLight(int index) {
  // Do nothing as we are controlling the lights with a timer
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return RoadSimulator();
  }
}
