<script lang="ts">
    import '../../../../app.css';

    import {page} from '$app/stores';

    let module = {
        moduleType: "quiz",
        questions: [{
            question: "What is 2+2?",
            questionOptions: ["4", "3", "5", "2"],
            answerIndex: 0,
        },
            {
                question: "What is 2+3?",
                questionOptions: ["4", "3", "5", "2"],
                answerIndex: 0,
            },
            {
                question: "What is 2+1?",
                questionOptions: ["4", "3", "5", "2"],
                answerIndex: 0,
            },
            {
                question: "What is 2+0?",
                questionOptions: ["4dsdsf", "3", "5", "2"],
                answerIndex: 0,
            },
        ]
    }
    // let module = {
    //     moduleType: "frq",
    //     question: "Why is the sky blue?"
    // }
    let activeIndex = 0;
    let selectedAnswer = -1;
    let questionsAnswered: number[] = [];
    let answersInputed = new Array(module.questions.length);
    function handleResponse(){
        if (selectedAnswer!= -1) {
            questionsAnswered.push(activeIndex);
            questionsAnswered = questionsAnswered;
            answersInputed[activeIndex] = selectedAnswer;
            console.log(answersInputed);
        }
        selectedAnswer = -1;
    }
    function scoreReport(){
        let correct = 0;
        for (let i = 0; i < answersInputed.length; i++) {
            if (answersInputed[i] === module.questions[i].answerIndex) {
                correct++;
            }
        }
        return "You got " + correct + "/" + answersInputed.length + " answers correct.";
    }

    function scoreNumeric(){
        let correct = 0;
        for (let i = 0; i < answersInputed.length; i++) {
            if (answersInputed[i] === module.questions[i].answerIndex) {
                correct++;
            }
        }

        return correct/answersInputed.length*100;
    }
    console.log(questionsAnswered.length);
    console.log(module.questions.length);
    $: complete = (questionsAnswered.length == module.questions.length);

</script>

<style>
    .quiz-container {
        max-width: 600px;
        margin: 0 auto;
        padding: 20px;
        background-color: #0e151a;
        color: #f5f5f5;
        border-radius: 10px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
    }

    .join {
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
    }

    .join-item {
        padding: 10px;
        margin: 0 5px;
        background-color: #333;
        color: #f5f5f5;
        border: none;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        font-size: 1rem;
        cursor: pointer;
    }

    .btn-active {
        background-color: #3a82f7;
        color: #fff;
        font-weight: bold;
    }

    .question {
        text-align: center;
        font-size: 1.5rem;
        margin-bottom: 15px;
    }

    .option {
        display: flex;
        align-items: center;
        padding: 10px;
        background-color: #152233;
        border-radius: 5px;
        margin-bottom: 10px;
    }

    .correct {
        display: flex;
        align-items: center;
        padding: 10px;
        background-color: #00FF00;
        border-radius: 5px;
        margin-bottom: 10px;
    }

    .incorrect {
        display: flex;
        align-items: center;
        padding: 10px;
        background-color: #EE4B2B;
        border-radius: 5px;
        margin-bottom: 10px;
    }

    .option input[type="radio"] {
        margin-right: 10px;
        accent-color: #3a82f7;
    }

    .submit-btn {
        display: block;
        width: 100%;
        padding: 12px;
        font-size: 1.1rem;
        background-color: #3a82f7;
        color: #fff;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        margin-top: 20px;
    }

    .submit-btn:hover {
        background-color: #316bc7;
    }
</style>
{#if module.moduleType === 'quiz'}
    {#if !complete}
    <div class="quiz-container">
        <div class="join">
            {#each {length: module.questions.length} as _, i}
                {#if i === activeIndex}
                    <button class="join-item btn btn-active">{i + 1}</button>
                {:else}
                    <button class="join-item btn" on:click={() => { activeIndex = i }}>{i + 1}</button>
                {/if}
            {/each}
        </div>

        <h1 class="question">
            {module.questions[activeIndex].question}
        </h1>
        {#if !questionsAnswered.includes(activeIndex)}
            {#each module.questions[activeIndex].questionOptions as option, i}
                <div class="option">
                    <input on:click={()=>{selectedAnswer=i}} type="radio" name="radio-{activeIndex}" id="option-{i}" class="radio"/>
                    <label for="option-{i}">{option}</label>
                </div>
            {/each}
            <button class="submit-btn" on:click={handleResponse}>
                Submit
            </button>
        {:else}
            {#each module.questions[activeIndex].questionOptions as option, i}
                <div class="option">
                    <input type="radio" name="radio-{activeIndex}" id="option-{i}" class="radio radio-error" disabled/>
                    <label for="option-{i}">{option}</label>
                </div>
            {/each}
        {/if}
    </div>
    {:else }
        <div class="quiz-container">
            <h1>
                Score Report:
            </h1>
            <div class="radial-progress text-primary" style="--value:{scoreNumeric()};" role="progressbar">{scoreNumeric()}%</div>
            <p>
                {scoreReport()}
            </p>
            <div class="join">
                {#each {length: module.questions.length} as _, i}
                    {#if i === activeIndex}
                        <button class="join-item btn btn-active">{i + 1}</button>
                    {:else}
                        <button class="join-item btn" on:click={() => { activeIndex = i }}>{i + 1}</button>
                    {/if}
                {/each}
            </div>

            {#each module.questions[activeIndex].questionOptions as option, i}
                {#if module.questions[activeIndex].answerIndex === i}
                    <div class="correct">
                        {option}
                    </div>
                {:else}
                    <div class="incorrect">
                        {option}
                    </div>

                {/if}
            {/each}
        </div>
    {/if}
{:else}
    <div class="quiz-container">
        <h1>
            here
            <!--{module.question}-->
        </h1>
    </div>
{/if}