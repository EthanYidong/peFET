import Navbar from "@/components/navbar";

export default function Home() {
  return (
    <>
      <Navbar />

      <section class="hero is-link is-fullheight-with-navbar">
        <div class="hero-body">
          <div>
            <p class="title">peFET</p>
            <p class="subtitle">Pre-event fast and easy testing</p>
          </div>
        </div>
      </section>
    </>
  );
}
