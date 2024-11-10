<script lang="ts">
    // Sample data for courses
    let file: File;
    const authorizedExtensions = ["pdf"];
    let courses = [
    {name:"Math 234", lastVisited:"2024-01-01", progress:"80%",id:"abc123"},
            {name:"Math 232", lastVisited:"2024-01-01", progress:"80%", id:"123abc"},
        ];

</script>


<h1 class="mb-4 text-4xl font-extrabold leading-none tracking-tight text-gray-900 md:text-5xl px-5 lg:text-6xl dark:text-white">
    Courses
</h1>

<div class="overflow-x-auto content-center px-5">
    <table class="table table-zebra w-mid">
        <thead>
        <tr>
            <th>Textbook Name</th>
            <th>Progress</th>
            <th>Last Visited</th>
        </tr>
        </thead>

        <tbody>
        {#each courses as course}
            <tr>
                <td>{course.name}</td>
                <td>{course.progress}</td>
                <td>{course.lastVisited}</td>
                <td>
                    <a href="/courses/{course.id}">
                        <button class="btn btn-success">
                            Open
                        </button>
                    </a>
                    <button class="btn btn-warning">
                    Delete
                    </button>
                </td>
            </tr>
        {/each}
        </tbody>
    </table>
<!--    <a href="#createmodal">-->
<!--        <button class="btn btn-primary">-->
<!--            Create New Course-->
<!--        </button>-->
<!--    </a>-->
    <button class="btn btn-primary" onclick={()=>my_modal_1.showModal()}>Upload PDF</button>
    <dialog id="my_modal_1" class="modal">
        <div class="modal-box">

            <div class="modal-action">
                <form action="?/avatar" method="post" enctype="multipart/form-data">
                    <input type="file" name="avatar" placeholder="avatar" />
                    <button class="btn btn-success" type="submit">Upload</button>
                </form>
                <form method="dialog">
                    <button class="btn btn-error">Close</button>
                </form>
            </div>
        </div>
    </dialog>
</div>


