from src.scheduler.tasks import scrape_task


# For triggering the scrape task manually
if __name__ == "__main__":
    scrape_task.delay() 
