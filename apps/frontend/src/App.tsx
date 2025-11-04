import "./App.css";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { RecipientsPage } from "@/components/RecipientsPage";
import { ArticlesPage } from "@/components/ArticlesPage";
import { EmailContentPage } from "@/components/EmailContentPage";

function App() {
	return (
		<div className="container mx-auto p-8 max-w-6xl">
			<div className="mb-8">
				<h1 className="text-4xl font-bold mb-2">News Pipeline Dashboard</h1>
				<p className="text-muted-foreground">Manage recipients, articles, and email content</p>
			</div>

			<Tabs defaultValue="recipients" className="w-full">
				<TabsList className="grid w-full grid-cols-3 mb-6">
					<TabsTrigger value="recipients" className="data-[state=active]:bg-blue-500 data-[state=active]:text-white">Recipients</TabsTrigger>
					<TabsTrigger value="articles" className="data-[state=active]:bg-blue-500 data-[state=active]:text-white">Articles</TabsTrigger>
					<TabsTrigger value="email-content" className="data-[state=active]:bg-blue-500 data-[state=active]:text-white">Email Content</TabsTrigger>
				</TabsList>
				<TabsContent value="recipients" >
					<RecipientsPage />
				</TabsContent>
				<TabsContent value="articles">
					<ArticlesPage />
				</TabsContent>
				<TabsContent value="email-content">
					<EmailContentPage />
				</TabsContent>
			</Tabs>
		</div>
	);
}

export default App;
