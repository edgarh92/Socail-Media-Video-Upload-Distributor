
from dataclasses import dataclass
import datetime
import argparse
from sum_media_duration import format_duration_to_seconds, get_total_duration
from _utils import build_file_list


@dataclass
class JobBatch:
    duration: datetime.timedelta = None
    assignment: str = None
    files: list = None


class UploadBatch():

    def __init__(self, JobBatch) -> None:
        self.MediaBatch = JobBatch

    def get_platform_table(self) -> dict:
        #Database Schema asserttion needed
        #Total Seconds
        #callDatabase()
        platform_db = {}
        platform_db["Youtube"] = 200
        platform_db["Instagram"]= 20000
        platform_db["TikTok"] = 20000
        return platform_db

    def is_valid_order(self, duration_db: dict) -> bool:

        """ Calculate Latest platform Duration,
            estimated final duration, and platform to platform duration
            Calculate Latest Database Duration
            platform Ratio

        Returns:
            bool: Trigger caption order through mediawen if ratio is below required target.
        """    
        #Calculate Ratio and Updates Database

        #Date Time Object as Seconds
        db_duration_as_sec = datetime.timedelta().total_seconds()
        batch_duration = self.MediaBatch.duration

        for captioned_duration in duration_db.values():
            db_duration_as_sec += captioned_duration

        try:            
            platform_duration_from_db = duration_db[self.MediaBatch.assignment]
            print("Stored platform Duration:", platform_duration_from_db)
        except:
            print('platform Does not exists')
        
        estimated_final_duration = ( batch_duration + platform_duration_from_db)
        db_duration_as_sec = (estimated_final_duration + db_duration_as_sec)
        platform_ratio = (estimated_final_duration/db_duration_as_sec) #Calculate
        print(f'Values: \
            {platform_ratio}, {db_duration_as_sec}, {estimated_final_duration}')
        #If the addition of these durations is greater than 10% it won't order captions
        #
        if platform_ratio < float(.10): #This needs work.
            #This will add contiously. 
            #If the ratio is greater than 10 it will add to the total
            print("Commit to platformDuration")
            print("Commit to updateDatabase")
            print("Commit to orderCaptions")
            return True
        else:
            #Keep to Rev
            print("Commit to platformDuration")
            print("Commit to updateDatabase")
            return False
        

    def platform_transaction(self, is_valid_order) -> None:
        '''Excute Captions Transaction'''


    def determine_platform_ratio(self) -> bool:

        self.MediaBatch.duration = format_duration_to_seconds(get_total_duration(
            video_file_list=self.MediaBatch.files)
            )
        platform_db = self.get_platform_table()
        is_valid_transaction = self.is_valid_order(platform_db)
        return is_valid_transaction



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Upload a video to social mediia based on total duration of existing social media uploads")
    parser.add_argument("-f", "--files", nargs="*", help="Indivudal files or directories to process")

    args = parser.parse_args()
    batch = JobBatch(
        duration=None,
        assignment='Youtube',
        files=build_file_list(args.files))
    if not batch.files:
        print('No accepted files found. Drag files or folders or both.')
    else:
        batch_transaction = UploadBatch(batch)
        transaction_status = batch_transaction.determine_platform_ratio()
        if transaction_status:
            print("Ordered Captions")
            batch_transaction.platform_transaction(transaction_status)

        else:
            print("no captions")
        