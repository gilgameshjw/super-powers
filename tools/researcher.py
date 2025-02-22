
import nest_asyncio # required for notebooks
nest_asyncio.apply()

from gpt_researcher import GPTResearcher
import asyncio

# report_types = ["research_report", "subtopic_report"]


async def get_report(query: str, report_type: str) -> str:
    researcher = GPTResearcher(query, report_type)
    research_result = await researcher.conduct_research()
    report = await researcher.write_report()

    # Get additional information
    research_context = researcher.get_research_context()
    research_costs = researcher.get_costs()
    research_images = researcher.get_research_images()
    research_sources = researcher.get_research_sources()

    return report, research_context, research_costs, research_images, research_sources


def run_researcher(query: str, report_type: str) -> str:
    research_report, research_context, research_costs, research_images, research_sources = asyncio.run(get_report(query, report_type))
    print("costs::///////////////////////////////////////////////")
    # save to file
    print(research_costs)
    with open("checks/costs.txt", "w") as f:
        f.write(str(research_costs))
    print("report::///////////////////////////////////////////////")
    with open("checks/report.txt", "w") as f:
        f.write(research_report)
    print("context::///////////////////////////////////////////////")
    with open("checks/context.txt", "w") as f:
        f.write(str(research_context))
    print(research_context)
    print("images::///////////////////////////////////////////////")
    with open("checks/images.txt", "w") as f:
        f.write(str(research_images))
    print(research_images)
    print("sources::///////////////////////////////////////////////")
    with open("checks/sources.txt", "w") as f:
        f.write(str(research_sources))
    print(research_sources)
    return research_report, research_costs