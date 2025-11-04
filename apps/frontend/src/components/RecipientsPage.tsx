import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { PlusIcon } from "lucide-react";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Spinner } from "@/components/ui/spinner";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { fetchRecipients } from "@/lib/api";
import { CreateRecipientModal } from "@/components/CreateRecipientModal";

export function RecipientsPage() {
	const [isModalOpen, setIsModalOpen] = useState(false);

	const {
		data: recipients = [],
		isLoading,
		isError,
		error,
	} = useQuery({
		queryKey: ["recipients"],
		queryFn: fetchRecipients,
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
						<span className="text-muted-foreground">Loading recipients...</span>
					</div>
				) : recipients.length === 0 ? (
					<div className="text-center py-12">
						<p className="text-muted-foreground">No recipients found</p>
					</div>
				) : (
					<div className="space-y-4">
						<div className="flex items-center justify-between">
							<div>
								<Badge variant="secondary" className="text-sm">
									{recipients.length} Total Recipients
								</Badge>
							</div>
							<Button onClick={() => setIsModalOpen(true)}>
								<PlusIcon />
								Add Recipient
							</Button>
						</div>

						<div className="rounded-md border">
							<Table>
								<TableHeader>
									<TableRow>
										<TableHead className="w-24">ID</TableHead>
										<TableHead>Name</TableHead>
										<TableHead>Email</TableHead>
									</TableRow>
								</TableHeader>
								<TableBody>
									{recipients.map((recipient) => (
										<TableRow key={recipient.id}>
											<TableCell className="font-medium">{recipient.id}</TableCell>
											<TableCell>{recipient.name}</TableCell>
											<TableCell className="text-muted-foreground">{recipient.email}</TableCell>
										</TableRow>
									))}
								</TableBody>
							</Table>
						</div>
					</div>
				)}
			</Card>

			<CreateRecipientModal open={isModalOpen} onOpenChange={setIsModalOpen} />
		</div>
	);
}

