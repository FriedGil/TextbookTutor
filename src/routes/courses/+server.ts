import path from 'path';
import fs from 'fs/promises';
import { fail } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

export const config = {
    runtime: 'edge',
};

export const POST = (async ({ request }) => {
    const stream = new ReadableStream({
        async start(controller) {
            try {
                const data = Object.fromEntries(await request.formData());
                const fileType = (data.avatar as Blob).type.split('/')[1];
                const filePath = path.join(
                    process.cwd(),
                    'static',
                    'avatars',
                    `${crypto.randomUUID()}.${fileType}`
                );

                controller.enqueue(`Saving file at ${filePath}\n`);

                // Write the file in chunks
                const buffer = Buffer.from(await (data.avatar as Blob).arrayBuffer());
                await fs.writeFile(filePath, buffer);

                // Send file path as JSON response
                const responseObj = { path: filePath };
                controller.enqueue(JSON.stringify(responseObj));

                // Close the stream
                controller.close();
            } catch (err) {
                controller.error(fail(500, { err }));
            }
        }
    });

    return new Response(stream, {
        headers: { 'Content-Type': 'application/json; charset=utf-8' },
    });
}) satisfies RequestHandler;
