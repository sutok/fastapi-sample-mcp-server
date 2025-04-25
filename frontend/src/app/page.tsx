import { Grid } from "@/components/layout/Grid/Grid";
import { Container } from "@/components/layout/Container/Container";

export default function Home() {
  return (
    <main>
      {/* ヒーローセクション */}
      <section className="py-12 md:py-20">
        <Container>
          <div className="text-center">
            <h1 className="text-3xl md:text-5xl font-bold mb-4">
              Welcome to Your App
            </h1>
            <p className="text-lg md:text-xl text-gray-600 max-w-2xl mx-auto mb-8">
              Next.js 13 with App Router and Tailwind CSS
            </p>
            <div className="space-x-4">
              <button className="px-6 py-3 bg-primary-600 text-white rounded-md hover:bg-primary-700 transition-colors">
                Get Started
              </button>
              <button className="px-6 py-3 border border-primary-600 text-primary-600 rounded-md hover:bg-primary-50 transition-colors">
                Learn More
              </button>
            </div>
          </div>
        </Container>
      </section>

      {/* フィーチャーセクション */}
      <section className="py-12 bg-gray-50">
        <Container>
          <Grid columns={{ sm: 1, md: 2, lg: 3 }} gap={6}>
            {[1, 2, 3].map((item) => (
              <div key={item} className="bg-white p-6 rounded-lg shadow-sm">
                <h3 className="text-xl font-semibold mb-3">Feature {item}</h3>
                <p className="text-gray-600">
                  Description of feature {item} and its benefits.
                </p>
              </div>
            ))}
          </Grid>
        </Container>
      </section>
    </main>
  );
}
