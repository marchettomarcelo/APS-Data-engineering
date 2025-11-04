const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export interface Recipient {
	id: number;
	name: string;
	email: string;
}

export interface CreateRecipientData {
	name: string;
	email: string;
}

export interface Article {
	id: number;
	url: string;
	title: string | null;
	content: string | null;
}

export interface EmailContent {
	id: number;
	subject: string | null;
	content: string | null;
	created_at: string | null;
}

export async function fetchRecipients(): Promise<Recipient[]> {
	const response = await fetch(`${API_BASE_URL}/recipients`);

	if (!response.ok) {
		throw new Error(`Failed to fetch recipients: ${response.statusText}`);
	}

	return response.json();
}

export async function createRecipient(data: CreateRecipientData): Promise<Recipient> {
	const response = await fetch(`${API_BASE_URL}/recipients`, {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify(data),
	});

	if (!response.ok) {
		const error = await response.json().catch(() => ({ detail: response.statusText }));
		throw new Error(error.detail || "Failed to create recipient");
	}

	return response.json();
}

export async function fetchArticles(): Promise<Article[]> {
	const response = await fetch(`${API_BASE_URL}/articles`);

	if (!response.ok) {
		throw new Error(`Failed to fetch articles: ${response.statusText}`);
	}

	return response.json();
}

export async function fetchEmailContent(): Promise<EmailContent[]> {
	const response = await fetch(`${API_BASE_URL}/email-content`);

	if (!response.ok) {
		throw new Error(`Failed to fetch email content: ${response.statusText}`);
	}

	return response.json();
}
