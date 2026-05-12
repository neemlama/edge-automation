<!DOCTYPE html>
<html>
<body>
    <h1>My first PHP page</h1>

    <?php
    $color="red";
    echo $color;
    echo "Hello World!", "This is multiple parameters."; //faster than print and can take multiple parameters while print needs contatenation
    $txt1="Studying php";
    $txt2="learning php";
    echo '<h2>' . $txt1 . '</h2>';
    echo '<p>' . "Day 1 of  " . $txt2 . '</p>';
    $cars=array("Volvo","BMW","Toyota");
    print_r($cars);
    class Car{
        public $color;
        public $model;
        public function __construct($color,$model){
            $this->color=$color;
            $this->model=$model;
        }
        public function message(){
            return "My car is a " . $this->color . " " . $this->model . "!";
        }
    }
    $mycar=new Car("black","Volvo");
    var_dump($mycar);
    $z='hello';
    $z=null;
    var_dump($z);
    echo phpversion(    )
    ?>
    
<body>
</html>
