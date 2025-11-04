import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Spinner } from "@/components/ui/spinner";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { fetchEmailContent } from "@/lib/api";
import DOMPurify from "dompurify";
import { Eye } from "lucide-react";

export function EmailContentPage() {
	const [selectedEmail, setSelectedEmail] = useState<any>(null);
	const {
		data: emailContents = [],
		isLoading,
		isError,
		error,
	} = useQuery({
		queryKey: ["emailContent"],
		queryFn: fetchEmailContent,
	});

	// Sort by created_at, newest first
	const sortedEmailContents = [...emailContents].sort((a, b) => {
		if (!a.created_at) return 1;
		if (!b.created_at) return -1;
		return new Date(b.created_at).getTime() - new Date(a.created_at).getTime();
	});

	const formatDate = (dateString: string | null) => {
		if (!dateString) return "Unknown date";
		const date = new Date(dateString);
		return date.toLocaleString("en-US", {
			year: "numeric",
			month: "short",
			day: "numeric",
			hour: "2-digit",
			minute: "2-digit",
		});
	};

	return (
		<div>
			{isError && (
				<Alert variant="destructive" className="mb-6">
					<AlertDescription>{error instanceof Error ? error.message : "An error occurred"}</AlertDescription>
				</Alert>
			)}

			{isLoading ? (
				<Card className="p-6">
					<div className="flex items-center justify-center py-12">
						<Spinner className="mr-2" />
						<span className="text-muted-foreground">Loading email content...</span>
					</div>
				</Card>
			) : sortedEmailContents.length === 0 ? (
				<Card className="p-6">
					<div className="text-center py-12">
						<p className="text-muted-foreground">No email content found</p>
					</div>
				</Card>
			) : (
				<div className="space-y-4">
					<div className="flex items-center justify-between mb-4">
						<Badge variant="secondary" className="text-sm">
							{sortedEmailContents.length} Total Email{sortedEmailContents.length !== 1 ? "s" : ""}
						</Badge>
					</div>

					<Card>
						<CardContent className="p-0">
							<div className="divide-y">
								{sortedEmailContents.map((email) => (
									<div key={email.id} className="flex items-center justify-between p-4 hover:bg-muted/50 transition-colors">
										<div className="flex-1 min-w-0 mr-4">
											<div className="flex items-center gap-3">
												<Badge variant="outline" className="shrink-0">
													ID: {email.id}
												</Badge>
												<h3 className="font-medium truncate">{email.subject || <span className="text-muted-foreground italic">No subject</span>}</h3>
											</div>
											<p className="text-sm text-muted-foreground mt-1">{formatDate(email.created_at)}</p>
										</div>
										<Button variant="outline" size="sm" onClick={() => setSelectedEmail(email)} className="shrink-0">
											<Eye className="h-4 w-4 mr-2" />
											View
										</Button>
									</div>
								))}
							</div>
						</CardContent>
					</Card>
				</div>
			)}

			{/* Email Content Modal */}
			<Dialog open={!!selectedEmail} onOpenChange={(open) => !open && setSelectedEmail(null)}>
				<DialogContent className="max-w-4xl max-h-[80vh] overflow-y-auto bg-white">
					<DialogHeader>
						<DialogTitle>{selectedEmail?.subject || <span className="text-muted-foreground italic">No subject</span>}</DialogTitle>
						<DialogDescription>
							<div className="flex items-center gap-3 mt-2">
								<Badge variant="outline">ID: {selectedEmail?.id}</Badge>
								<span>{formatDate(selectedEmail?.created_at)}</span>
							</div>
						</DialogDescription>
					</DialogHeader>
					<div className="mt-4">
						{selectedEmail?.content ? (
							<div
								className="prose prose-sm max-w-none [&_a]:text-blue-600 [&_a]:underline [&_img]:max-w-full [&_img]:h-auto"
								dangerouslySetInnerHTML={{
									__html: DOMPurify.sanitize(selectedEmail.content, {
										ALLOWED_TAGS: ["b", "i", "em", "strong", "a", "p", "br", "ul", "ol", "li", "h1", "h2", "h3", "h4", "h5", "h6", "img", "div", "span", "table", "thead", "tbody", "tr", "th", "td", "blockquote", "code", "pre"],
										ALLOWED_ATTR: ["href", "src", "alt", "title", "style", "class"],
									}),
								}}
							/>
						) : (
							<p className="text-muted-foreground italic">No content</p>
						)}
					</div>
				</DialogContent>
			</Dialog>
		</div>
	);
}
