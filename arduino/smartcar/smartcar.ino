#include <Array.h>

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  char command = Serial.read();
  priorityQueue(command);
}

void priorityQueue(char command) {
  const int ARRAY_MAX = 100;
  boolean previousCommand;

  Array<String, ARRAY_MAX> array;
  unsigned int arr_start = 0;

  while (array.size() > 0) {
    array[arr_start] = command;
    if (previousCommand) {
      if (Serial.println(command)) {
        previousCommand = true;
        arr_start ++;
      } else {
        Serial.print("Something is wrong with the queue.");
      }
    }
  }
}
