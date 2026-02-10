import { NextResponse } from "next/server";

const BACKEND_URL =
    "https://chat-security-backend-175245796032.us-central1.run.app";

export async function POST(req: Request) {
    const body = await req.json();

    const res = await fetch(`${BACKEND_URL}/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
    });

    const data = await res.json();
    return NextResponse.json(data, { status: res.status });
}