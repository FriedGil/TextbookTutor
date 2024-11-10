import path from 'path'
import fs from 'fs/promises'
import { fail, redirect } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

export const POST = (async ({ request, url }) => {
    try {
        const data = Object.fromEntries(await request.formData())
        const filePath = path.join(
            process.cwd(),
            "static",
            "avatars",
            `${crypto.randomUUID()}.${((data.avatar as Blob).type.split("/")[1])}`
        );
        await fs.writeFile(filePath, Buffer.from(await (data.avatar as Blob).arrayBuffer()))
        // TODO: store the file path in database for further references.
        return new Response(String({path: filePath}))
    } catch (err) {
        throw fail(500, { err: err })
    }
}) satisfies RequestHandler;