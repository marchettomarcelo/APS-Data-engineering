import { useQuery } from "@tanstack/react-query";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Spinner } from "@/components/ui/spinner";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { fetchArticles } from "@/lib/api";

export function ArticlesPage() {
	const {
		data: articles = [],
		isLoading,
		isError,
		error,
	} = useQuery({
		queryKey: ["articles"],
		queryFn: fetchArticles,
	});

	return (
		<div>
			{isError && (
				<Alert variant="destructive" className="mb-6">
					<AlertDescription>{error instanceof Error ? error.message : "An error occurred"}</AlertDescription>
				</Alert>
			)}

			<Card className="p-6">
				{isLoading ? (
					<div className="flex items-center justify-center py-12">
						<Spinner className="mr-2" />
						<span className="text-muted-foreground">Loading articles...</span>
					</div>
				) : articles.length === 0 ? (
					<div className="text-center py-12">
						<p className="text-muted-foreground">No articles found</p>
					</div>
				) : (
					<div className="space-y-4">
						<div className="flex items-center justify-between">
							<div>
								<Badge variant="secondary" className="text-sm">
									{articles.length} Total Articles
								</Badge>
							</div>
						</div>

						<div className="rounded-md border">
							<Table>
								<TableHeader>
									<TableRow>
										<TableHead className="w-24">ID</TableHead>
										<TableHead className="w-1/3">Title</TableHead>
										<TableHead>URL</TableHead>
									</TableRow>
								</TableHeader>
								<TableBody>
									{articles.map((article) => (
										<TableRow key={article.id}>
											<TableCell className="font-medium">{article.id}</TableCell>
											<TableCell>
												{article.title || <span className="text-muted-foreground italic">No title</span>}
											</TableCell>
											<TableCell className="text-muted-foreground">
												<a 
													href={article.url} 
													target="_blank" 
													rel="noopener noreferrer"
													className="hover:underline truncate block max-w-md"
													title={article.url}
												>
													{article.url}
												</a>
											</TableCell>
										</TableRow>
									))}
								</TableBody>
							</Table>
						</div>
					</div>
				)}
			</Card>
		</div>
	);
}

