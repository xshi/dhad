#include "HadronicDNtupleProc/HadronicDTuple.h"
#include <string.h>
#include <iostream>

HadronicDTuple::HadronicDTuple() {
   clear();
#include "HadronicDNtupleProc/tuple_init.h"
}

void HadronicDTuple::clear() {
   memset(&run, 0, (&end_marker - &run)*sizeof(int));
/*   int* one = &run;
   for (; one < &end_marker; one++) {
      std::cout << *one << std::endl;
      } */
}
