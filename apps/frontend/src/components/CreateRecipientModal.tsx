import { useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { createRecipient, type CreateRecipientData } from "@/lib/api";
import {
	Dialog,
	DialogContent,
	DialogDescription,
	DialogFooter,
	DialogHeader,
	DialogTitle,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Spinner } from "@/components/ui/spinner";

interface CreateRecipientModalProps {
	open: boolean;
	onOpenChange: (open: boolean) => void;
}

export function CreateRecipientModal({ open, onOpenChange }: CreateRecipientModalProps) {
	const [formData, setFormData] = useState<CreateRecipientData>({
		name: "",
		email: "",
	});
	const queryClient = useQueryClient();

	const mutation = useMutation({
		mutationFn: createRecipient,
		onSuccess: () => {
			queryClient.invalidateQueries({ queryKey: ["recipients"] });
			setFormData({ name: "", email: "" });
			onOpenChange(false);
		},
	});

	const handleSubmit = (e: React.FormEvent) => {
		e.preventDefault();
		mutation.mutate(formData);
	};

	const handleClose = () => {
		if (!mutation.isPending) {
			setFormData({ name: "", email: "" });
			mutation.reset();
			onOpenChange(false);
		}
	};

	return (
		<Dialog open={open} onOpenChange={handleClose}>
			<DialogContent className="sm:max-w-[425px] bg-white">
				<DialogHeader>
					<DialogTitle className="text-black cursor-pointer">Add New Recipient</DialogTitle>
					<DialogDescription>
						Create a new email recipient. Click save when you're done.
					</DialogDescription>
				</DialogHeader>

				<form onSubmit={handleSubmit}>
					<div className="grid gap-4 py-4">
						{mutation.isError && (
							<Alert variant="destructive">
								<AlertDescription>
									{mutation.error instanceof Error
										? mutation.error.message
										: "An error occurred"}
								</AlertDescription>
							</Alert>
						)}

						<div className="grid gap-2">
							<Label htmlFor="name">Name</Label>
							<Input
								id="name"
								value={formData.name}
								onChange={(e) => setFormData({ ...formData, name: e.target.value })}
								placeholder="John Doe"
								required
								disabled={mutation.isPending}
							/>
						</div>

						<div className="grid gap-2">
							<Label htmlFor="email">Email</Label>
							<Input
								id="email"
								type="email"
								value={formData.email}
								onChange={(e) => setFormData({ ...formData, email: e.target.value })}
								placeholder="john@example.com"
								required
								disabled={mutation.isPending}
							/>
						</div>
					</div>

					<DialogFooter>
						<Button
							type="button"
							variant="outline"
							onClick={handleClose}
							disabled={mutation.isPending}
						>
							Cancel
						</Button>
						<Button type="submit" disabled={mutation.isPending}>
							{mutation.isPending && <Spinner className="mr-2" />}
							Save Recipient
						</Button>
					</DialogFooter>
				</form>
			</DialogContent>
		</Dialog>
	);
}

