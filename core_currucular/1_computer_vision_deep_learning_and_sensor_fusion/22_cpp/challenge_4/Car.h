// Your code goes here!
// Take a look at Car.cpp to see how to define the Car class.
#ifndef CAR_H
#define CAR_H

// Hint: you'll need to define:

// 1. the class itself
class Car {

	// 2. the class constructor
	public: Car();

	// 3. one private property
	private: bool in_working_condition_;

	// 4. three public methods
	public: void wearAndTear();
	public: bool drive();
	public: void fix();
 
};

#endif  // CAR_H