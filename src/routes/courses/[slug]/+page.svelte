<script>
    import { page } from '$app/stores';
    import '../../../app.css';

    let chapters = [
        {number:1, name:"Addition", modules:[1.1,1.2,1.3]},
        {number:2, name:"Subtraction", modules:[2.1,2.2,2.3]},
        {number:3, name:"Multiplication", modules:[3.1,3.2,3.3]},
        {number:4, name:"Division", modules:[4.1,4.2,4.3]},

    ]
</script>


<div>

<h1 class="mb-4 text-4xl font-extrabold leading-none tracking-tight text-gray-900 md:text-5xl px-5 lg:text-6xl dark:text-white">{$page.params.slug}
</h1>

{#each chapters as chapter}
    <div tabindex="-1" class="collapse bg-base-200">
        <div class="collapse-title text-xl font-medium">{chapter.name}</div>
        <div class="collapse-content">
            <div class="overflow-x-auto">
                <table class="table table-zebra">
                    <thead>
                    <tr>
                        <th>Module</th>
                        <th>Type</th>
                        <th>Completion</th>
                        <th>Score</th>

                    </tr>
                    </thead>
                    <tbody>
                    {#each chapter.modules as module}
                        <tr>
                            <td>{module}</td>
                            <td>Activity</td>
                            <td>100%</td>
                            <td>60%</td>
                            <td>
                                <a href="/courses/{$page.params.slug}/quiz">
                                    <button class="btn btn-success">
                                        Start
                                    </button>
                                </a>
                            </td>

                        </tr>
                        <tr>
                            <td>{module}</td>
                            <td>Quiz</td>
                            <td>50%</td>
                            <td/>
                            <td>
                                <a href="/courses/{$page.params.slug}/quiz">
                                    <button class="btn btn-success">
                                        Start
                                    </button>
                                </a>
                            </td>

                        </tr>
                    {/each}

                    </tbody>
                </table>
            </div>
        </div>
    </div>
{/each}
</div>