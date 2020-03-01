package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"reflect"
	"strconv"
	"sync"
	"time"
)

func hello(str string, num int, b bool) string {
	time.Sleep(time.Second * 1)
	return fmt.Sprintf("str=%s num=%d b=%t", str, num, b)
}

func main() {
	log.SetOutput(ioutil.Discard)

	workers := 3
	arguments := []interface{}{
		[]interface{}{"hello1", 1, true},
		[]interface{}{"hello2", 2, true},
		[]interface{}{"hello3", 3, true},
		[]interface{}{"hello4", 4, true},
		[]interface{}{"hello5", 5, true},
		[]interface{}{"hello6", 6, true},
		[]interface{}{"hello7", 7, true},
	}

	callback := func(input []interface{}, output []reflect.Value) {
		/*
			This function will be executed when hello is finished
		*/
		fmt.Printf("Executed hello %v, returned: %v\n", input, output)
	}

	status := runWorkersPool(
		reflect.ValueOf(hello),
		interface2map(arguments),
		callback,
		workers,
	)

	if status == true {
		fmt.Println("Workers finished")
	}

}

var wg sync.WaitGroup

type callBackFn func(input []interface{}, output []reflect.Value)

func unpackAndCall(target reflect.Value, args []interface{}) []reflect.Value {
	var functionArr []reflect.Value
	for _, arg := range args {
		functionArr = append(functionArr, reflect.ValueOf(arg))
	}
	return target.Call(functionArr)
}

func worker(id int, target reflect.Value, jobs chan []interface{}, input chan []interface{}, output chan []reflect.Value) {
	defer func() {
		log.Println("We broke from the loop somehow?")
	}()
	for job := range jobs {
		wg.Add(1)
		log.Printf("Worker-%d is running\n", id)

		/*
			This may have a racing condition?
		*/
		output <- unpackAndCall(target, job)
		input <- job

		log.Printf("Worker-%d is finished\n", id)
		wg.Done()
	}
}

func interface2map(in []interface{}) map[int]([]interface{}) {
	mymap := make(map[int]([]interface{}))
	for idx, item := range in {
		mymap[idx] = item.([]interface{})
	}
	return mymap
}

func divisableBy(num int) (int, int) {
	/*
		TODO: this is not efficient try something else
	*/
	for i := 2; i <= 1000; i++ {
		if num%i == 0 {
			return i, i
		}
	}
	return 1, 1
}

func runWorkersPool(target reflect.Value, allArgs map[int]([]interface{}), callback callBackFn, workers int) bool {

	jobs := make(chan []interface{})
	input := make(chan []interface{}, workers)
	output := make(chan []reflect.Value, workers)
	runningWorkers := 0

	for id := 1; id < workers; id++ {
		go worker(id, target, jobs, input, output)
		log.Printf("Spawned new worker with id=%d", id)
	}

	tworkers := len(allArgs)
	for idx, args := range allArgs {
		runningWorkers++
		jobs <- args
		if runningWorkers >= workers {
			wg.Wait()
			for i := 0; i < runningWorkers; i++ {
				callback(<-input, <-output)
			}
			runningWorkers = 0
		}
		tworkers -= workers
		if tworkers < 0 {
			/*
				TODO: this code is every messy. simplify it more
				TODO: current approche may have some bugs detecting remaining items. change it
			*/
			workers, tworkers = divisableBy(idx - workers)
			log.Println("Arguments is not enough to start workers. new workers=" + strconv.Itoa(workers))
		}

	}

	return true

}
