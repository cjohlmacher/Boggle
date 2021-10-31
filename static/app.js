console.log('This script is active');

const TIME_LIMIT = 60000;

const $form = $("form");
const $message = $(".message")
const $wordSubmit = $(".word-submission")
const $score = $(".score")
const $timer = $(".timer")
$timer.text(TIME_LIMIT/1000);
$message.hide()

let gameOver = false;

//Submit guess to server
const makeGuess = async (guess) => {
    res = axios({
        method: 'post',
        url: '/submit-guess',
        data: {
            guess: guess
        }
    });
    return res
};

//Increment score for valid guess
const incrementScore = (value) => {
    let currentScore = parseInt($score.text());
    $score.text(currentScore+value);
}

//Start the timer for the game
const startTimer = (timeLimit) => {
    let countdown = setInterval(decrementTime,1000);
    setTimeout(async () => {
        decrementTime();
        clearInterval(countdown);
        gameOver = true;
        $message.text("Time's up!");
        isHighScore = await submitScore($score.text());
        console.log('High Score?', isHighScore);
    },timeLimit);
};

//Submit the user's score to the server
const submitScore = async (score) => {
    res = axios({
        method: 'post',
        url: '/submit-score',
        data: {
            'score': score
        }
    });
    return res
}

//Countdown time
const decrementTime = () => {
    let currentTime = parseInt($timer.text());
    $timer.text(currentTime-1);
}

guessResponses = {
    'ok': {
        response: "Great guess!",
        animation: 'flash-green',
    },
    'not-on-board': {
        response: "That word isn't on the board!",
        animation: 'flash-red',
    },
    'not-word': {
        response: "Sorry, that's not a word",
        animation: 'flash-red',
    },
    'already-guessed': {
        response: "Already used that word!",
        animation: 'flash-blue',
    }
}

//Handler for submitting a guess
const handleFormSubmit = async (e) => {
    e.preventDefault();
    let $guess = $("input").val()
    if (!gameOver) {
        res = await makeGuess($guess);
        displayMessage(res);
        if (res.data.Result === "ok") {
            incrementScore($guess.length);
        };
    };
    $("input").val("");
}

//Display Message on Guess Submit
const displayMessage = (res) => {
    message_text = guessResponses[res.data.Result]['response'];
    $message.text(message_text);
    $message.show();
    $wordSubmit.addClass(guessResponses[res.data.Result]['animation'])
    setTimeout( (animation) => {
        $wordSubmit.removeClass(animation)
    },1000,guessResponses[res.data.Result]['animation']);
}

$form.on('submit', handleFormSubmit);

startTimer(TIME_LIMIT);